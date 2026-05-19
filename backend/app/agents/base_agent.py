from abc import ABC, abstractmethod
from typing import Dict
from backend.app.services.ai_client import AIClient
from backend.app.services.retries import retry_on_exception


class BaseAgent(ABC):
    def __init__(self, workflow_id: int):
        self.workflow_id = workflow_id
        self.ai_client = AIClient()

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, context: Dict) -> str:
        raise NotImplementedError

    def execute(self, context: Dict) -> Dict:
        prompt = self.build_prompt(context)
        return self._call_ai(prompt)

    @retry_on_exception()
    def _call_ai(self, prompt: str) -> Dict:
        return self.ai_client.call(prompt)
