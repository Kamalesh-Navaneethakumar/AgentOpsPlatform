from backend.app.agents.base_agent import BaseAgent


class PriorityClassificationAgent(BaseAgent):
    def name(self) -> str:
        return "priority_classification"

    def build_prompt(self, context: dict) -> str:
        return (
            "You are an enterprise priority classification agent. "
            "Analyze the document and extracted tasks, then assign a priority level to the workflow: low, normal, high, or urgent. "
            "Provide a short rationale.\n\n"
            f"Document:\n{context['input_document']}\n\n" 
            f"Existing tasks:\n{context.get('tasks', [])}"
        )
