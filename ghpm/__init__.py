# -*- coding: utf-8 -*-
"""entrypoint."""
import sys

from loguru import logger

logger.remove()
fmt = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <lvl>{message}</lvl>"
)
logger.add(sys.stderr, format=fmt)
