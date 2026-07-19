# Unified Data Model (Single Tableau Data Source)

This replaces the earlier approach of one separate data source per chart. Instead,
all 8 cleaned tables are combined into **one Tableau data source** using Tableau's
**Relationships** (not the older "Joins" feature) — this is what allows one filter
to control every chart, without the row-multiplication ("fan-out") bug that a
plain SQL/physical join would cause when combining tables at different levels of
detail.

## Table grain (the most important thing to get right)

| Table | One row = | Primary key |
|---|---|---|
| `orders` | one order | `order_id` |
| `order_items` | one line item within an order | `order_id` + `order_item_id` |
| `order_payments` | one payment installment on an order | `order_id` + `payment_sequential` |
| `order_reviews` | one review of an order | `review_id` + `order_id` |
| `customers` | one customer | `customer_id` |
| `products` | one product | `product_id` |
| `sellers` | one seller | `seller_id` |
| `geolocation` | one ZIP-code prefix | `geolocation_zip_code_prefix` |

`orders` is the hub. `order_items`, `order_payments`, and `order_reviews` are all
"many rows per order" — this is exactly why joining them directly to each other
would multiply rows incorrectly. Relationships avoid this by aggregating each
side to the order grain *before* combining them, only when a view actually mixes
fields from two many-side tables.

## Relationships to build

| Table A | Field | Table B | Field | Cardinality |
|---|---|---|---|---|
| `orders` | `customer_id` | `customers` | `customer_id` | many orders : one customer |
| `order_items` | `order_id` | `orders` | `order_id` | many items : one order |
| `order_items` | `product_id` | `products` | `product_id` | many items : one product |
| `order_items` | `seller_id` | `sellers` | `seller_id` | many items : one seller |
| `order_payments` | `order_id` | `orders` | `order_id` | many payments : one order |
| `order_reviews` | `order_id` | `orders` | `order_id` | many reviews : one order |
| `customers` | `customer_zip_code_prefix` | `geolocation` | `geolocation_zip_code_prefix` | many customers : one ZIP |

(`sellers.seller_zip_code_prefix` → `geolocation` is optional — only add it if you
end up needing seller-location mapping; skip it to keep the model simpler.)

## Calculated fields you'll need to recreate

The old per-chart data sources used pre-built SQL views that already computed
things like `order_total`, `month`, and `delivery_days`. In the single-source
model, these become **Tableau calculated fields** instead, built on top of the
raw tables:

- **`Order Total`** = `[price] + [freight_value]` (on `order_items`)
- **`Order Month`** = `DATETRUNC('month', [order_purchase_timestamp])` (on `orders`)
- **`Delivery Days`** = `DATEDIFF('day', [order_purchase_timestamp], [order_delivered_customer_date])` (on `orders`)
- **`Delivered On Time`** = `IF [order_delivered_customer_date] <= [order_estimated_delivery_date] THEN 1 ELSE 0 END`
- **`Delivery Bucket`** = a `CASE`/`IF` on `Delivery Days` grouping into "0-9 days", "10-19 days", etc.
- **`Day of Week`** = `DATENAME('weekday', [order_purchase_timestamp])`

## What this enables

Because every chart now pulls from the same data source, a single filter or
parameter placed on the dashboard (e.g. a date range, a state picker) will
automatically affect every chart at once — solving the exact problem your
manager raised.
