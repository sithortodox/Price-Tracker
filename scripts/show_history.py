from app.db import SessionLocal
from app.models import PriceHistory, TrackedProduct


def main() -> None:
    with SessionLocal() as session:
        products = session.query(TrackedProduct).all()
        if not products:
            print("No tracked products found")
            return

        for product in products:
            print(f"\n=== {product.title} (id={product.id}) ===")
            rows = (
                session.query(PriceHistory)
                .filter_by(product_id=product.id)
                .order_by(PriceHistory.checked_at.asc(), PriceHistory.id.asc())
                .all()
            )
            if not rows:
                print("No history yet")
                continue
            for row in rows:
                print(
                    f"{row.checked_at.isoformat()} | price={row.price} | in_stock={row.in_stock}"
                )


if __name__ == "__main__":
    main()
