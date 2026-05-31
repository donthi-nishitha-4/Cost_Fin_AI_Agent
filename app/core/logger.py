import logging
import sys

from app.core.settings import settings


def setup_logger():
    logger = logging.getLogger("cost_finance_agent")
    level_name = settings.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()