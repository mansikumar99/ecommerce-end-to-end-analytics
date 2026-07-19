"""Clean the raw Olist Brazilian E-Commerce CSVs and write tidy versions to data/processed/."""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

DATE_COLUMNS = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_order_items_dataset.csv": ["shipping_limit_date"],
    "olist_order_reviews_dataset.csv": ["review_creation_date", "review_answer_timestamp"],
}


def load_raw(filename: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / filename)
    for col in DATE_COLUMNS.get(filename, []):
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_customers() -> pd.DataFrame:
    df = load_raw("olist_customers_dataset.csv")
    df = df.drop_duplicates(subset="customer_id")
    df["customer_city"] = df["customer_city"].str.title().str.strip()
    df["customer_state"] = df["customer_state"].str.upper().str.strip()
    return df


def clean_sellers() -> pd.DataFrame:
    df = load_raw("olist_sellers_dataset.csv")
    df = df.drop_duplicates(subset="seller_id")
    df["seller_city"] = df["seller_city"].str.title().str.strip()
    df["seller_state"] = df["seller_state"].str.upper().str.strip()
    return df


def clean_products() -> pd.DataFrame:
    df = load_raw("olist_products_dataset.csv")
    translation = load_raw("product_category_name_translation.csv")
    df = df.drop_duplicates(subset="product_id")

    # Fill missing category with a placeholder, then map to English name
    df["product_category_name"] = df["product_category_name"].fillna("unknown")
    df = df.merge(translation, on="product_category_name", how="left")
    df["product_category_name_english"] = df["product_category_name_english"].fillna(
        df["product_category_name"]
    )

    # Presentation formatting: "cds_dvds_musicals" -> "Cds Dvds Musicals",
    # so category names read cleanly on charts without a display-only calc field.
    df["product_category_name_english"] = (
        df["product_category_name_english"].str.replace("_", " ", regex=False).str.title().str.strip()
    )
    df["product_category_name"] = (
        df["product_category_name"].str.replace("_", " ", regex=False).str.title().str.strip()
    )

    numeric_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df = df.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )
    return df[
        [
            "product_id",
            "product_category_name",
            "product_category_name_english",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
    ]


def clean_orders() -> pd.DataFrame:
    df = load_raw("olist_orders_dataset.csv")
    df = df.drop_duplicates(subset="order_id")
    df["order_status"] = df["order_status"].str.lower().str.strip()
    # Orders that were never approved/delivered legitimately have null delivery dates;
    # keep as NaT rather than dropping rows, since order_status already explains why.
    return df


def clean_order_items() -> pd.DataFrame:
    df = load_raw("olist_order_items_dataset.csv")
    df = df.drop_duplicates()
    df = df[(df["price"] > 0) & (df["freight_value"] >= 0)]
    return df


def clean_order_payments() -> pd.DataFrame:
    df = load_raw("olist_order_payments_dataset.csv")
    df = df.drop_duplicates()
    df = df[df["payment_value"] >= 0]
    df["payment_type"] = (
        df["payment_type"].str.replace("_", " ", regex=False).str.title().str.strip()
    )
    return df


def clean_order_reviews() -> pd.DataFrame:
    df = load_raw("olist_order_reviews_dataset.csv")
    # A handful of review_ids repeat for the same order (resubmitted surveys); keep latest answer
    df = df.sort_values("review_answer_timestamp").drop_duplicates(
        subset=["review_id", "order_id"], keep="last"
    )
    for col in ["review_comment_title", "review_comment_message"]:
        df[col] = df[col].fillna("")
    return df


def clean_geolocation() -> pd.DataFrame:
    df = load_raw("olist_geolocation_dataset.csv")
    # Collapse to one averaged lat/lng per zip prefix; raw file has many noisy duplicates per prefix
    df = (
        df.groupby("geolocation_zip_code_prefix")
        .agg(
            geolocation_lat=("geolocation_lat", "mean"),
            geolocation_lng=("geolocation_lng", "mean"),
            geolocation_city=("geolocation_city", "first"),
            geolocation_state=("geolocation_state", "first"),
        )
        .reset_index()
    )
    df["geolocation_city"] = df["geolocation_city"].str.title().str.strip()
    df["geolocation_state"] = df["geolocation_state"].str.upper().str.strip()
    return df


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    tables = {
        "customers": clean_customers(),
        "sellers": clean_sellers(),
        "products": clean_products(),
        "orders": clean_orders(),
        "order_items": clean_order_items(),
        "order_payments": clean_order_payments(),
        "order_reviews": clean_order_reviews(),
        "geolocation": clean_geolocation(),
    }

    for name, df in tables.items():
        out_path = PROCESSED_DIR / f"{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"{name:16s} -> {len(df):>7,} rows -> {out_path.name}")


if __name__ == "__main__":
    main()
