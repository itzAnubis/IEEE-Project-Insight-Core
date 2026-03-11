import logging
import sys

from app.core.config import LOG_LEVEL


def setup_logging(level: str = LOG_LEVEL) -> logging.Logger:
    """Create and configure the application logger."""

    _logger = logging.getLogger("insight_api")
    _logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not _logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        _logger.addHandler(handler)

    return _logger


logger = setup_logging()
