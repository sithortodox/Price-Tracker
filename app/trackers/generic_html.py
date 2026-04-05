from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup

from app.trackers.base import BaseTracker, ProductSnapshot


def _extract_text_by_selector(soup: BeautifulSoup, selector: str | None) -> str | None:
    if not selector:
        return None
    node = soup.select_one(selector)
    if node is None:
        return None
    text = node.get_text(" ", strip=True)
    return text or None


def _parse_price(value: str | None) -> float | None:
    if not value:
        return None
    cleaned = value.replace("\xa0", " ")
    match = re.search(r"(\d+[\d\s,.]*)", cleaned)
    if not match:
        return None
    number = match.group(1).replace(" ", "").replace(",", ".")
    try:
        return float(number)
    except ValueError:
        return None


class GenericHtmlTracker(BaseTracker):
    source_name = "generic_html"

    def __init__(
        self,
        *,
        title_selector: str,
        price_selector: str,
        in_stock_selector: str | None = None,
        out_of_stock_text: str | None = None,
    ) -> None:
        self.title_selector = title_selector
        self.price_selector = price_selector
        self.in_stock_selector = in_stock_selector
        self.out_of_stock_text = (out_of_stock_text or "").strip().lower()

    def can_handle(self, url: str) -> bool:
        return url.startswith("http://") or url.startswith("https://")

    async def fetch_snapshot(self, url: str) -> ProductSnapshot:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        title = _extract_text_by_selector(soup, self.title_selector)
        price_text = _extract_text_by_selector(soup, self.price_selector)
        stock_text = _extract_text_by_selector(soup, self.in_stock_selector)
        price = _parse_price(price_text)

        in_stock = True
        if stock_text and self.out_of_stock_text:
            in_stock = self.out_of_stock_text not in stock_text.lower()

        return ProductSnapshot(
            title=title,
            price=price,
            in_stock=in_stock,
            currency="RUB",
            source=self.source_name,
            raw_payload=html[:5000],
        )
