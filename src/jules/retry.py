import time
import logging

logger = logging.getLogger("jules.retry")

def retry_request(func, retries=3, backoff=0.5):
    last_exception = None
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            # Only retry on things that look like transport errors or 5xx/429
            # In this simplified model, we'll just retry a few times
            logger.warning(f"Request failed (attempt {i+1}/{retries}): {e}")
            if i < retries - 1:
                time.sleep(backoff * (2 ** i))

    raise last_exception
