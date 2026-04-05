from app.db import SessionLocal
from app.models import TrackedProduct


def main() -> None:
    with SessionLocal() as session:
        existing = session.query(TrackedProduct).filter_by(url="https://example.com/product/demo-console").first()
        if existing:
            print("Demo product already exists")
            return

        product = TrackedProduct(
            source="generic_html",
            title="Demo Console",
            url="https://example.com/product/demo-console",
            sku="DEMO-CONSOLE-001",
            currency="RUB",
            target_price=49990,
            selectors={
                "title": "h1",
                "price": ".price",
                "stock": ".availability",
                "out_of_stock_text": "нет в наличии",
            },
            is_active=True,
        )
        session.add(product)
        session.commit()
        print("Demo product created")


if __name__ == "__main__":
    main()
