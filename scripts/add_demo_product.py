from app.db import SessionLocal
from app.models import TrackedProduct


def main() -> None:
    url = input("Product URL: ").strip()
    title = input("Title: ").strip() or "Demo tracked product"
    source = input("Source [generic_html]: ").strip() or "generic_html"
    currency = input("Currency [RUB]: ").strip() or "RUB"

    with SessionLocal() as session:
        existing = session.query(TrackedProduct).filter_by(url=url).first()
        if existing:
            print("Product already exists")
            return

        product = TrackedProduct(
            source=source,
            title=title,
            url=url,
            currency=currency,
            is_active=True,
        )
        session.add(product)
        session.commit()
        print(f"Added product id={product.id}")


if __name__ == "__main__":
    main()
