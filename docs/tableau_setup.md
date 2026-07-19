# Connecting Tableau to this database

The cleaned data lives in a MySQL/MariaDB server (via XAMPP) on this machine. Tableau
Desktop needs one extra driver to talk to MySQL — it isn't bundled with Tableau.

## 1. Install the MySQL driver

1. Go to Tableau's driver download page: https://www.tableau.com/support/drivers
2. Choose **MySQL** from the connector list.
3. Download and install **MySQL Connector/C 6.1** (or the ODBC driver, either works)
   for Windows, matching your Tableau bit-ness (64-bit, almost always).
4. This is a small (~15-20MB) installer — no need to install a full MySQL server,
   just the client driver.

## 2. Make sure the database server is running

This project runs its own MySQL/MariaDB instance (separate from your regular XAMPP
MySQL, to avoid touching your other project databases). Start it with:

```bash
cd /e/xamp/mysql/bin
./mysqld.exe --datadir="E:\ecommerce-analytics-project\mysql_data" --port=3307 \
  --socket="E:\ecommerce-analytics-project\mysql_data\mysql.sock"
```

Leave this running in its own terminal window while you use Tableau.

## 3. Connect from Tableau Desktop

1. Open Tableau Desktop → **Connect** → **To a Server** → **More...** → **MySQL**.
2. Enter:
   - **Server**: `127.0.0.1`
   - **Port**: `3307`
   - **Database**: `ecommerce_analytics`
   - **Username**: `root`
   - **Password**: see `.env` in the project root (not committed to git)
3. Click **Sign In**.

## 4. Choose your data source

You have two options — use the pre-built views (recommended):

- Under the database, select any of the `vw_*` views (e.g. `vw_monthly_revenue`,
  `vw_category_performance`, `vw_state_performance`, `vw_order_items_detail`,
  `vw_review_summary`, `vw_customer_order_counts`). These already do the
  heavy joins/aggregation in SQL (see `sql/views.sql`).
- Or use **New Custom SQL** and paste a query directly, e.g. to combine two views
  or add extra filtering before Tableau sees the data.

## 5. Recommended dashboard sheets

Built from the views above:

1. **Revenue trend** — line chart of `vw_monthly_revenue` (month vs. revenue),
   with a dual-axis for order_count.
2. **Category performance** — bar chart of `vw_category_performance` (revenue by
   category, sorted descending), color by `pct_delivered_on_time`.
3. **Geo revenue map** — filled map of `vw_state_performance` (Brazilian states,
   revenue), using the state abbreviation as the geographic field (set the
   `customer_state` field's geographic role to allow custom Brazil state mapping,
   or use `Latitude (generated)`/`Longitude (generated)` joined from the raw
   `geolocation` table if you need finer-grained mapping).
4. **Delivery performance** — KPI tiles: avg delivery days, % delivered on time,
   from `vw_order_items_detail`.
5. **Review score vs. category** — scatter/bar of `vw_review_summary`.
6. **Payment mix** — pie/bar of payment_type from the `order_payments` table.

Combine these into one dashboard with a date filter (order month) and a state
filter acting across all sheets.
