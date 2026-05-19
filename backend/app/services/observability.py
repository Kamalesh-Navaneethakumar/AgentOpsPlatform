from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def build_observation(agent_name: str, prompt: str, response: str, latency_ms: int, retries: int, status: str, error_message: str = None) -> Dict[str, Any]:
    observation = {
        "agent_name": agent_name,
        "prompt": prompt,
        "response_snippet": response[:512],
        "latency_ms": latency_ms,
        "retries": retries,
        "status": status,
    }
    if error_message:
        observation["error_message"] = error_message
    logger.info("Observation created: %s", observation)
    return observation
