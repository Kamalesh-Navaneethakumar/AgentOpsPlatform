from backend.app.agents.base_agent import BaseAgent


class SummarizationAgent(BaseAgent):
    def name(self) -> str:
        return "summarization"

    def build_prompt(self, context: dict) -> str:
        return (
            "You are a corporate summarization agent. "
            "Read the document and produce an executive summary that is concise, actionable, and suitable for leadership review. "
            "Include bullets for the problem, recommendation, and business impact.\n\n"
            f"Document:\n{context['input_document']}"
        )
