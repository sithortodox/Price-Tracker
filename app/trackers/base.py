from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductSnapshot:
    title: str | None
    price: float | None
    in_stock: bool
    currency: str | None = None
    source: str | None = None
    raw_payload: str | None = None


class BaseTracker:
    source_name = "base"

    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    async def fetch_snapshot(self, url: str) -> ProductSnapshot:
        raise NotImplementedError
