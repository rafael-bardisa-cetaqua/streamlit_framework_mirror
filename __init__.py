from .src.logger import logger
def set_verbosity(level: int):
    logger.setLevel(level)

__all__ = ["auth", "pages", "state", "set_verbosity"]
