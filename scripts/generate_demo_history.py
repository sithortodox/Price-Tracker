from datetime import datetime, timedelta, timezone

from app.db import SessionLocal
from app.models import PriceHistory, TrackedProduct
from app.plotting import build_price_plot


def main() -> None:
    with SessionLocal() as session:
        product = session.query(TrackedProduct).filter_by(url="https://example.com/product/demo-console").first()
        if product is None:
            print("Demo product not found. Run seed_demo_data.py first.")
            return

        session.query(PriceHistory).filter_by(product_id=product.id).delete()

        now = datetime.now(timezone.utc)
        demo_points = [
            (now - timedelta(days=12), 56990, False),
            (now - timedelta(days=9), 55990, False),
            (now - timedelta(days=6), 54990, True),
            (now - timedelta(days=3), 52990, True),
            (now, 49990, True),
        ]

        for checked_at, price, in_stock in demo_points:
            session.add(
                PriceHistory(
                    product_id=product.id,
                    price=price,
                    in_stock=in_stock,
                    raw_title=product.title,
                    raw_payload=f"demo_price={price};in_stock={in_stock}",
                    checked_at=checked_at,
                )
            )

        session.commit()

        labels = [point[0].strftime("%d.%m") for point in demo_points]
        values = [point[1] for point in demo_points]
        output = build_price_plot(list(zip(labels, values)), "artifacts/demo_price_history.png")
        print(f"Demo history created. Plot saved to: {output}")


if __name__ == "__main__":
    main()
