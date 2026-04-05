from __future__ import annotations

import logging

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def send_telegram_message(text: str) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logger.info("Telegram notifier skipped: config missing")
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": settings.telegram_chat_id,
        "text": text,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, json=payload)
    response.raise_for_status()
    return True
