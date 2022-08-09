# -*- coding: utf-8 -*-
"""entrypoint."""

import sys

from loguru import logger

logger.remove()


def formatter(record: dict) -> str:
    """Dynamic log formatter."""
    if record["level"].name == "DEBUG":
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <lvl>{message}</lvl>\n"
        )
    else:
        return "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <lvl>{message}</lvl>\n"


logger.add(sys.stderr, format=formatter)
