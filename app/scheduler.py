from __future__ import annotations

import asyncio
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def run_scheduler() -> None:
    logger.info("Scheduler started with interval=%s seconds", settings.check_interval_seconds)
    while True:
        logger.info("Tick: placeholder product check cycle")
        await asyncio.sleep(settings.check_interval_seconds)
