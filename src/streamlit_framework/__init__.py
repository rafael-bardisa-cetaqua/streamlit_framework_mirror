from .src.logger import logger
def set_verbosity(level: int):
    """
    set the verbosity level of the framework logger
    """
    logger.setLevel(level)

__version__ = "0.1.2"

__all__ = ["auth", "pages", "state", "style", "structure", "set_verbosity"]
