"""Logging configuration for the EnformionGO API wrapper."""

import logging
import os
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercepts standard logging messages and redirects them to Loguru."""

    def emit(self, record):
        """Emits the record.

        Args:
            record: The record.
        """
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    """Sets up the logging for the application."""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logging.basicConfig(handlers=[InterceptHandler()], level=0)