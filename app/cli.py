from __future__ import annotations

import argparse
import asyncio
import json

from sqlalchemy import select

from app.db import SessionLocal
from app.models import PriceHistory, TrackedProduct
from app.service import run_check_cycle
from app.trackers.generic_html import GenericHtmlTracker


def cmd_list(_: argparse.Namespace) -> None:
    with SessionLocal() as session:
        products = session.execute(select(TrackedProduct).order_by(TrackedProduct.id.asc())).scalars().all()
        if not products:
            print("No tracked products found")
            return

        for product in products:
            print(
                f"id={product.id} | active={product.is_active} | source={product.source} | "
                f"title={product.title} | url={product.url}"
            )


def cmd_add(args: argparse.Namespace) -> None:
    selectors = None
    if args.selectors:
        selectors = json.loads(args.selectors)

    with SessionLocal() as session:
        existing = session.execute(select(TrackedProduct).where(TrackedProduct.url == args.url)).scalar_one_or_none()
        if existing is not None:
            print(f"Product already exists: id={existing.id}")
            return

        product = TrackedProduct(
            source=args.source,
            title=args.title,
            url=args.url,
            sku=args.sku,
            currency=args.currency,
            target_price=args.target_price,
            selectors=selectors,
            is_active=True,
        )
        session.add(product)
        session.commit()
        print(f"Added product id={product.id}")


def cmd_history(args: argparse.Namespace) -> None:
    with SessionLocal() as session:
        product = session.execute(select(TrackedProduct).where(TrackedProduct.id == args.id)).scalar_one_or_none()
        if product is None:
            print("Product not found")
            return

        rows = session.execute(
            select(PriceHistory)
            .where(PriceHistory.product_id == product.id)
            .order_by(PriceHistory.checked_at.asc(), PriceHistory.id.asc())
        ).scalars().all()

        print(f"=== {product.title} (id={product.id}) ===")
        if not rows:
            print("No history yet")
            return

        for row in rows:
            print(f"{row.checked_at.isoformat()} | price={row.price} | in_stock={row.in_stock}")


def cmd_deactivate(args: argparse.Namespace) -> None:
    with SessionLocal() as session:
        product = session.execute(select(TrackedProduct).where(TrackedProduct.id == args.id)).scalar_one_or_none()
        if product is None:
            print("Product not found")
            return

        product.is_active = False
        session.commit()
        print(f"Product {product.id} deactivated")


def cmd_delete(args: argparse.Namespace) -> None:
    with SessionLocal() as session:
        product = session.execute(select(TrackedProduct).where(TrackedProduct.id == args.id)).scalar_one_or_none()
        if product is None:
            print("Product not found")
            return

        session.delete(product)
        session.commit()
        print(f"Product {args.id} deleted")


def build_default_trackers() -> list[GenericHtmlTracker]:
    return [
        GenericHtmlTracker(
            title_selector="h1",
            price_selector="[data-price], .price, .product-price, .price__current",
            in_stock_selector=".availability, .stock, .product-availability",
            out_of_stock_text="нет в наличии",
        )
    ]


async def cmd_check_once(_: argparse.Namespace) -> None:
    await run_check_cycle(build_default_trackers())
    print("Check cycle completed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Price Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List tracked products")
    list_parser.set_defaults(func=cmd_list)

    add_parser = subparsers.add_parser("add", help="Add tracked product")
    add_parser.add_argument("--source", default="generic_html")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--url", required=True)
    add_parser.add_argument("--sku")
    add_parser.add_argument("--currency", default="RUB")
    add_parser.add_argument("--target-price", type=float)
    add_parser.add_argument("--selectors", help='JSON string, e.g. {"title":"h1","price":".price"}')
    add_parser.set_defaults(func=cmd_add)

    history_parser = subparsers.add_parser("history", help="Show product history")
    history_parser.add_argument("--id", type=int, required=True)
    history_parser.set_defaults(func=cmd_history)

    deactivate_parser = subparsers.add_parser("deactivate", help="Deactivate tracked product")
    deactivate_parser.add_argument("--id", type=int, required=True)
    deactivate_parser.set_defaults(func=cmd_deactivate)

    delete_parser = subparsers.add_parser("delete", help="Delete tracked product")
    delete_parser.add_argument("--id", type=int, required=True)
    delete_parser.set_defaults(func=cmd_delete)

    check_once_parser = subparsers.add_parser("check-once", help="Run one manual check cycle")
    check_once_parser.set_defaults(func=cmd_check_once)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = args.func(args)
    if asyncio.iscoroutine(result):
        asyncio.run(result)


if __name__ == "__main__":
    main()
