from backend.app.agents.base_agent import BaseAgent


class ReportingAgent(BaseAgent):
    def name(self) -> str:
        return "reporting"

    def build_prompt(self, context: dict) -> str:
        return (
            "You are an automated reporting agent for enterprise workflows. "
            "Use the analysis, summary, tasks, and priority information to generate a final report suitable for stakeholders. "
            "Include the current approval status, recommended next steps, and risk mitigation notes.\n\n"
            f"Summary:\n{context.get('summary', '')}\n\n"
            f"Analysis:\n{context.get('analysis', '')}\n\n"
            f"Tasks:\n{context.get('tasks', [])}\n\n"
            f"Priority:\n{context.get('priority', '')}"
        )
