from __future__ import annotations

import asyncio
import logging

from app.config import get_settings
from app.service import run_check_cycle
from app.trackers.generic_html import GenericHtmlTracker

logger = logging.getLogger(__name__)
settings = get_settings()


def build_default_trackers() -> list[GenericHtmlTracker]:
    return [
        GenericHtmlTracker(
            title_selector="h1",
            price_selector="[data-price], .price, .product-price, .price__current",
            in_stock_selector=".availability, .stock, .product-availability",
            out_of_stock_text="нет в наличии",
        )
    ]


async def run_scheduler() -> None:
    trackers = build_default_trackers()
    logger.info("Scheduler started with interval=%s seconds", settings.check_interval_seconds)
    while True:
        try:
            await run_check_cycle(trackers)
        except Exception as exc:
            logger.exception("Check cycle failed: %s", exc)
        await asyncio.sleep(settings.check_interval_seconds)
