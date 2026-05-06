import logging
import os
from datetime import datetime
from time import struct_time
from zoneinfo import ZoneInfo

import colorlog

__all__ = ("get_logger",)

LOG_LEVEL = os.getenv(key="LOG_LEVEL", default="INFO")


class Formatter(colorlog.ColoredFormatter):
    def converter(self, timestamp: float) -> struct_time:  # type: ignore
        return datetime.fromtimestamp(
            timestamp=timestamp, tz=ZoneInfo("America/Chicago")
        ).timetuple()


def _get_default_formatter(name: str) -> Formatter:
    """Return a default colorized formatter."""
    return Formatter(
        fmt=f"%(log_color)s[{name}][%(asctime)s][%(levelname)s] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        log_colors={
            "DEBUG": "white",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )


def get_logger(
    name: str, level: int | None = None, handler: logging.StreamHandler | None = None
) -> logging.Logger:
    """Create and return a colorized logger instance."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    log_level = level or getattr(logging, LOG_LEVEL.upper())

    logger.setLevel(log_level)
    logger.propagate = False

    if handler is None:
        handler = logging.StreamHandler()
    handler.setLevel(log_level)

    formatter = _get_default_formatter(name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
