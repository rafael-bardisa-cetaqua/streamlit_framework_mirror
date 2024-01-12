from .src.logger import logger
def set_verbosity(level: int):
    """
    set the verbosity level of the framework logger
    """
    logger.setLevel(level)

__all__ = ["auth", "pages", "state", "style", "set_verbosity"]
