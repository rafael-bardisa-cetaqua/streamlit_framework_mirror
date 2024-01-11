import logging
import sys


logger = logging.getLogger("streamlit_framework")

if logger.level is logging.NOTSET:
    logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    formatter = logging.Formatter(
        "\033[95m%(levelname)s\033[0m%(funcName)s %(lineno)s %(message)s"
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)