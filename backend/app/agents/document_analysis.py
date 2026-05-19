from backend.app.agents.base_agent import BaseAgent


class DocumentAnalysisAgent(BaseAgent):
    def name(self) -> str:
        return "document_analysis"

    def build_prompt(self, context: dict) -> str:
        return (
            "You are an enterprise document analysis agent. "
            "Extract the key business objectives, stakeholders, and action items from the document below. "
            "Provide a structured JSON summary with sections: objectives, stakeholders, risks, opportunities, and next_steps.\n\n"
            f"Document:\n{context['input_document']}"
        )
