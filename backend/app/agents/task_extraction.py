from backend.app.agents.base_agent import BaseAgent


class TaskExtractionAgent(BaseAgent):
    def name(self) -> str:
        return "task_extraction"

    def build_prompt(self, context: dict) -> str:
        return (
            "You are a task extraction agent for enterprise operations. "
            "Identify all discrete tasks, owners, due dates, and dependencies from the business document. "
            "Return the output as JSON array of tasks with fields: title, description, owner, priority, due_date, dependency.\n\n"
            f"Document:\n{context['input_document']}"
        )
