import time
import logging
from typing import Dict, Optional
from backend.app.config import AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY

logger = logging.getLogger(__name__)

try:
    import openai
except ImportError:
    openai = None


class AIClient:
    def __init__(self):
        if AI_PROVIDER == "openai" and openai is None:
            raise RuntimeError("openai package is required for OPENAI provider")
        self.provider = AI_PROVIDER
        self.api_key = OPENAI_API_KEY if AI_PROVIDER == "openai" else GEMINI_API_KEY

    def _format_response(self, response: Dict) -> str:
        if self.provider == "openai":
            return response["choices"][0]["message"]["content"].strip()
        return response.get("text", "").strip()

    def call(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512) -> Dict:
        start_time = time.time()
        if self.provider == "openai":
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt or "You are an enterprise AI assistant."},
                          {"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = self._format_response(response)
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "response": output,
                "raw": response,
                "latency_ms": latency_ms,
                "provider": self.provider,
            }
        raise NotImplementedError(f"AI provider {self.provider} is not implemented")
