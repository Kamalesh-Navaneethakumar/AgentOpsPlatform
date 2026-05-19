import json
from typing import Dict, Any, List
from backend.app.agents.document_analysis import DocumentAnalysisAgent
from backend.app.agents.summarization import SummarizationAgent
from backend.app.agents.task_extraction import TaskExtractionAgent
from backend.app.agents.priority_classification import PriorityClassificationAgent
from backend.app.agents.reporting import ReportingAgent
from backend.app.services.observability import build_observation
from backend.app import crud, schemas
from sqlalchemy.orm import Session


class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.agent_classes = [
            DocumentAnalysisAgent,
            SummarizationAgent,
            TaskExtractionAgent,
            PriorityClassificationAgent,
            ReportingAgent,
        ]

    def _log_agent(self, workflow_id: int, agent_name: str, prompt: str, response: str, status: str, latency_ms: int, retries: int, error_message: str = None):
        log = schemas.AgentLogCreate(
            workflow_id=workflow_id,
            agent_name=agent_name,
            prompt=prompt,
            response=response,
            status=status,
            latency_ms=latency_ms,
            retries=retries,
            error_message=error_message,
        )
        crud.create_agent_log(self.db, log)

    def run_workflow(self, workflow, approval_required: bool = True) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "input_document": workflow.input_document,
            "priority": workflow.priority,
            "tasks": workflow.tasks or [],
        }
        workflow.status = "running"
        self.db.add(workflow)
        self.db.commit()

        stages: List[Dict[str, Any]] = []
        for agent_class in self.agent_classes:
            agent = agent_class(workflow.id)
            response_data = {"response": "", "latency_ms": 0}
            try:
                call_result = agent.execute(context)
                response_text = call_result["response"]
                response_data = call_result
                status = "success"
            except Exception as exc:
                response_text = f"Agent failed: {exc}"
                status = "failed"
                self._log_agent(workflow.id, agent.name(), "", response_text, status, 0, 0, str(exc))
                workflow.status = "failed"
                self.db.add(workflow)
                self.db.commit()
                return {"workflow": workflow, "error": str(exc)}

            self._log_agent(
                workflow.id,
                agent.name(),
                agent.build_prompt(context),
                response_text,
                status,
                response_data.get("latency_ms", 0),
                0,
            )

            if agent.name() == "document_analysis":
                context["analysis"] = response_text
            elif agent.name() == "summarization":
                context["summary"] = response_text
            elif agent.name() == "task_extraction":
                try:
                    context["tasks"] = json.loads(response_text)
                except Exception:
                    context["tasks"] = [{"note": response_text}]
            elif agent.name() == "priority_classification":
                context["priority"] = response_text
            elif agent.name() == "reporting":
                workflow.output_summary = response_text

            stages.append({
                "agent": agent.name(),
                "status": status,
                "response": response_text,
            })

        workflow.tasks = context["tasks"]
        workflow.priority = context["priority"]
        workflow.status = "approval_pending" if approval_required else "completed"
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return {"workflow": workflow, "stages": stages}
