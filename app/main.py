from __future__ import annotations

import asyncio
import logging

from app.config import get_settings
from app.db import Base, engine
from app.scheduler import run_scheduler


def setup_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


async def main() -> None:
    setup_logging()
    init_db()
    await run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())
