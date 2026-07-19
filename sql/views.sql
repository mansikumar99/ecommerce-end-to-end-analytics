-- Analytical views for Tableau to connect to directly.
-- Keeping joins/aggregation in SQL keeps Tableau's own calculated fields
-- limited to lightweight, dashboard-level logic (filters, LOD tweaks, formatting).

USE ecommerce_analytics;

DROP VIEW IF EXISTS vw_order_items_detail;
DROP VIEW IF EXISTS vw_order_summary;
DROP VIEW IF EXISTS vw_monthly_revenue;
DROP VIEW IF EXISTS vw_category_performance;
DROP VIEW IF EXISTS vw_state_performance;
DROP VIEW IF EXISTS vw_review_summary;
DROP VIEW IF EXISTS vw_customer_order_counts;
DROP VIEW IF EXISTS vw_kpi_summary;
DROP VIEW IF EXISTS vw_delivery_distribution;
DROP VIEW IF EXISTS vw_weekday_orders;

-- One row per order item, enriched with order/customer/seller/product context
-- plus computed delivery timing. This is the main fact-level view.
CREATE VIEW vw_order_items_detail AS
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value)          AS item_total,
    p.product_category_name_english        AS category,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    c.customer_id,
    c.customer_unique_id,
    c.customer_state,
    c.customer_city,
    s.seller_state,
    s.seller_city,
    DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)  AS delivery_days,
    DATEDIFF(o.order_estimated_delivery_date, o.order_delivered_customer_date) AS delivery_vs_estimate_days,
    CASE
        WHEN o.order_delivered_customer_date IS NULL THEN NULL
        WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1
        ELSE 0
    END AS delivered_on_time
FROM order_items oi
JOIN orders o     ON oi.order_id = o.order_id
JOIN customers c  ON o.customer_id = c.customer_id
JOIN products p   ON oi.product_id = p.product_id
JOIN sellers s    ON oi.seller_id = s.seller_id;

-- One row per order, with order-level revenue and item count.
CREATE VIEW vw_order_summary AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_timestamp,
    c.customer_state,
    c.customer_city,
    COUNT(oi.order_item_id)              AS item_count,
    SUM(oi.price)                        AS items_total,
    SUM(oi.freight_value)                AS freight_total,
    SUM(oi.price + oi.freight_value)     AS order_total
FROM orders o
JOIN customers c    ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, c.customer_unique_id, o.order_status,
         o.order_purchase_timestamp, c.customer_state, c.customer_city;

-- Monthly revenue trend (excludes cancelled/unavailable orders).
CREATE VIEW vw_monthly_revenue AS
SELECT
    DATE(DATE_FORMAT(order_purchase_timestamp, '%Y-%m-01')) AS month,
    COUNT(DISTINCT order_id)   AS order_count,
    SUM(order_total)           AS revenue,
    AVG(order_total)           AS avg_order_value
FROM vw_order_summary
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY DATE(DATE_FORMAT(order_purchase_timestamp, '%Y-%m-01'));

-- Revenue, volume and delivery performance by product category.
CREATE VIEW vw_category_performance AS
SELECT
    category,
    COUNT(*)                       AS items_sold,
    SUM(item_total)                AS revenue,
    AVG(price)                     AS avg_price,
    AVG(delivery_days)             AS avg_delivery_days,
    AVG(delivered_on_time) * 100   AS pct_delivered_on_time
FROM vw_order_items_detail
GROUP BY category;

-- Revenue and order volume by customer state (for a geo map).
CREATE VIEW vw_state_performance AS
SELECT
    customer_state,
    COUNT(DISTINCT order_id)   AS order_count,
    SUM(order_total)           AS revenue,
    AVG(order_total)           AS avg_order_value
FROM vw_order_summary
GROUP BY customer_state;

-- Average review score and volume by category.
CREATE VIEW vw_review_summary AS
SELECT
    p.product_category_name_english AS category,
    AVG(r.review_score)             AS avg_review_score,
    COUNT(*)                        AS review_count
FROM order_reviews r
JOIN order_items oi ON r.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english;

-- Orders per unique customer, for repeat-purchase-rate calculations.
CREATE VIEW vw_customer_order_counts AS
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id;

-- Single-row headline KPIs: total revenue, total orders, true avg order value
-- (total revenue / total orders, not an average of monthly averages).
CREATE VIEW vw_kpi_summary AS
SELECT
    SUM(order_total)                          AS total_revenue,
    COUNT(DISTINCT order_id)                  AS total_orders,
    SUM(order_total) / COUNT(DISTINCT order_id) AS avg_order_value
FROM vw_order_summary
WHERE order_status NOT IN ('canceled', 'unavailable');

-- Delivery time distribution, bucketed, one row per delivered order.
CREATE VIEW vw_delivery_distribution AS
SELECT
    CASE
        WHEN delivery_days BETWEEN 0 AND 9   THEN '0-9 days'
        WHEN delivery_days BETWEEN 10 AND 19 THEN '10-19 days'
        WHEN delivery_days BETWEEN 20 AND 29 THEN '20-29 days'
        WHEN delivery_days BETWEEN 30 AND 39 THEN '30-39 days'
        WHEN delivery_days BETWEEN 40 AND 49 THEN '40-49 days'
        ELSE '50+ days'
    END AS delivery_bucket,
    CASE
        WHEN delivery_days BETWEEN 0 AND 9   THEN 1
        WHEN delivery_days BETWEEN 10 AND 19 THEN 2
        WHEN delivery_days BETWEEN 20 AND 29 THEN 3
        WHEN delivery_days BETWEEN 30 AND 39 THEN 4
        WHEN delivery_days BETWEEN 40 AND 49 THEN 5
        ELSE 6
    END AS bucket_sort_order,
    COUNT(*) AS total_orders
FROM (
    SELECT
        order_id,
        DATEDIFF(order_delivered_customer_date, order_purchase_timestamp) AS delivery_days
    FROM orders
    WHERE order_delivered_customer_date IS NOT NULL
) delivered
GROUP BY delivery_bucket, bucket_sort_order;

-- Order volume by day of week, with a numeric column for correct Mon-Sun sorting.
CREATE VIEW vw_weekday_orders AS
SELECT
    DAYNAME(order_purchase_timestamp)                        AS day_of_week,
    (DAYOFWEEK(order_purchase_timestamp) + 5) % 7             AS day_sort_order,
    COUNT(DISTINCT order_id)                                  AS total_orders
FROM orders
GROUP BY day_of_week, day_sort_order;
