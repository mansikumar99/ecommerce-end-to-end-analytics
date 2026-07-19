"""Create the MySQL schema and load the cleaned Olist CSVs into it."""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"

load_dotenv(BASE_DIR / ".env")

DB_HOST = os.environ["MYSQL_HOST"]
DB_PORT = os.environ["MYSQL_PORT"]
DB_USER = os.environ["MYSQL_USER"]
DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
DB_NAME = os.environ["MYSQL_DATABASE"]

# Load order matters: tables with no foreign keys first, then dependents.
TABLE_LOAD_ORDER = [
    "customers",
    "sellers",
    "products",
    "geolocation",
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
]


def run_schema(engine) -> None:
    lines = [
        line
        for line in SCHEMA_FILE.read_text().splitlines()
        if not line.strip().startswith("--")
    ]
    statements = [s.strip() for s in "\n".join(lines).split(";") if s.strip()]
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for stmt in statements:
            conn.execute(text(stmt))
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def load_tables(engine) -> None:
    for table in TABLE_LOAD_ORDER:
        csv_path = PROCESSED_DIR / f"{table}.csv"
        df = pd.read_csv(csv_path)
        df.to_sql(table, engine, if_exists="append", index=False, chunksize=5000)
        print(f"{table:16s} -> loaded {len(df):>7,} rows")


def main() -> None:
    # Connect to the server (no database yet) to create it, then reconnect scoped to it.
    server_engine = create_engine(
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
    )
    run_schema(server_engine)

    db_engine = create_engine(
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    load_tables(db_engine)


if __name__ == "__main__":
    main()
