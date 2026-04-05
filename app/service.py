from __future__ import annotations

import logging
from typing import Iterable

from sqlalchemy import select

from app.db import SessionLocal
from app.models import PriceHistory, TrackedProduct
from app.notifier import send_telegram_message
from app.trackers.base import BaseTracker, ProductSnapshot
from app.trackers.generic_html import GenericHtmlTracker

logger = logging.getLogger(__name__)


def _snapshot_changed(previous: PriceHistory | None, snapshot: ProductSnapshot) -> bool:
    if previous is None:
        return True
    previous_price = previous.price
    previous_stock = previous.in_stock
    return previous_price != snapshot.price or previous_stock != snapshot.in_stock


def _build_change_message(product: TrackedProduct, snapshot: ProductSnapshot, previous: PriceHistory | None) -> str:
    previous_price = previous.price if previous else None
    previous_stock = previous.in_stock if previous else None
    return (
        f"📦 {product.title}\n"
        f"Источник: {product.source}\n"
        f"Цена: {snapshot.price} {snapshot.currency or product.currency}\n"
        f"В наличии: {'да' if snapshot.in_stock else 'нет'}\n"
        f"Было: цена={previous_price}, наличие={'да' if previous_stock else 'нет' if previous is not None else 'n/a'}\n"
        f"URL: {product.url}"
    )


async def run_check_cycle(trackers: Iterable[BaseTracker]) -> None:
    tracker_list = list(trackers)
    if not tracker_list:
        logger.info("No trackers configured for check cycle")
        return

    with SessionLocal() as session:
        products = session.execute(select(TrackedProduct).where(TrackedProduct.is_active.is_(True))).scalars().all()

        for product in products:
            tracker = next((item for item in tracker_list if item.can_handle(product.url)), None)
            if tracker is None and product.source == "generic_html":
                tracker = GenericHtmlTracker.from_selectors(product.selectors)
            if tracker is None:
                logger.warning("No tracker found for product id=%s url=%s", product.id, product.url)
                continue

            try:
                snapshot = await tracker.fetch_snapshot(product.url)
            except Exception as exc:
                logger.warning("Tracker fetch failed for product id=%s: %s", product.id, exc)
                continue

            previous = session.execute(
                select(PriceHistory)
                .where(PriceHistory.product_id == product.id)
                .order_by(PriceHistory.checked_at.desc(), PriceHistory.id.desc())
                .limit(1)
            ).scalar_one_or_none()

            history_row = PriceHistory(
                product_id=product.id,
                price=snapshot.price,
                in_stock=snapshot.in_stock,
                raw_title=snapshot.title,
                raw_payload=snapshot.raw_payload,
            )
            session.add(history_row)

            if snapshot.title and snapshot.title != product.title:
                product.title = snapshot.title
            if snapshot.currency:
                product.currency = snapshot.currency

            changed = _snapshot_changed(previous, snapshot)
            session.commit()

            if changed:
                try:
                    await send_telegram_message(_build_change_message(product, snapshot, previous))
                except Exception as exc:
                    logger.warning("Notifier failed for product id=%s: %s", product.id, exc)
