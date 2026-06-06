import time
import logging
from typing import Dict, Optional
from backend.app.config import AI_PROVIDER, GEMINI_API_KEY

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class AIClient:
    def __init__(self):
        if AI_PROVIDER == "gemini" and genai is None:
            raise RuntimeError("google-generativeai package is required for Gemini provider")
        self.provider = AI_PROVIDER
        self.api_key = GEMINI_API_KEY
        if self.provider == "gemini":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")

    def call(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512) -> Dict:
        start_time = time.time()
        if self.provider == "gemini":
            full_prompt = f"{system_prompt or 'You are an enterprise AI assistant.'}\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            output = response.text.strip() if response.text else "No response generated"
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "response": output,
                "raw": response,
                "latency_ms": latency_ms,
                "provider": self.provider,
            }
        raise NotImplementedError(f"AI provider {self.provider} is not implemented")
