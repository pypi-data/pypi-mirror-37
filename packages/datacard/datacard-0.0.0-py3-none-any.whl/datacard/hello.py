import logging

logger = logging.getLogger(__name__)

def greeting_text(name: str) -> str:
    logger.debug(f"Making a greeting for {name}")
    return f"Hello, {name}!"
