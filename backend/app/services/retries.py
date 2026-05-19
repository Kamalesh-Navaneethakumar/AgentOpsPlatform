import time
import logging
from functools import wraps
from backend.app.config import RETRY_BACKOFF_SECONDS, RETRY_MAX_ATTEMPTS

logger = logging.getLogger(__name__)


def retry_on_exception():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    attempt += 1
                    logger.warning("Retry attempt %s for %s: %s", attempt, fn.__name__, exc)
                    if attempt >= RETRY_MAX_ATTEMPTS:
                        logger.error("Max retry attempts reached for %s", fn.__name__)
                        raise
                    time.sleep(RETRY_BACKOFF_SECONDS * attempt)
        return wrapper
    return decorator
