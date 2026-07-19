# E-Commerce Analytics Project

An end-to-end analytics pipeline for the [Olist Brazilian E-Commerce Public
Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): raw CSVs
→ Python cleaning → MySQL → SQL analytical views → Tableau dashboard.

## Project structure

```
ecommerce-analytics-project/
├── data/
│   ├── raw/            # original Olist CSVs (gitignored, not committed)
│   └── processed/      # cleaned CSVs output by src/clean_data.py (gitignored)
├── src/
│   ├── clean_data.py       # cleans raw CSVs -> data/processed/
│   └── load_to_mysql.py    # creates schema + loads processed CSVs into MySQL
├── sql/
│   ├── schema.sql       # table definitions (customers, orders, products, ...)
│   └── views.sql        # analytical views used by Tableau (revenue, category,
│                         # state, review, delivery, customer-repeat views)
├── docs/
│   ├── tableau_setup.md # how to install the MySQL driver and connect Tableau
│   └── data_model.md    # unified data model: 8 base tables + Tableau Relationships
├── reports/
│   └── analysis_report.md  # written analysis with headline findings
├── tableau/              # Tableau workbook (.twbx) and dashboard screenshots
├── requirements.txt
└── .gitignore
```

## Dataset

**Source:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(Kaggle). Real, anonymized commercial data: ~99,441 orders placed on the Olist
marketplace between Sep 2016 and Sep 2018, across 9 relational tables
(customers, orders, order items, payments, reviews, products, sellers,
geolocation, and a category-name translation table).

## Setup

### 1. Python environment

```bash
python -m venv .venv
./.venv/Scripts/pip install -r requirements.txt
```

### 2. Get the raw data

Download `dataset.zip` from the Kaggle link above and extract all 9 CSVs into
`data/raw/`.

### 3. Clean the data

```bash
./.venv/Scripts/python src/clean_data.py
```

This reads `data/raw/*.csv`, fixes dtypes (dates, numerics), removes
duplicates, fills missing values, translates product category names to
English, and collapses noisy geolocation duplicates — writing tidy CSVs to
`data/processed/`.

### 4. Set up MySQL and load the data

Create a `.env` file in the project root (not committed — see `.gitignore`):

```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3308
MYSQL_USER=root
MYSQL_PASSWORD=<your local password>
MYSQL_DATABASE=ecommerce_analytics
```

Start your MySQL/MariaDB server, then run:

```bash
./.venv/Scripts/python src/load_to_mysql.py
```

This applies `sql/schema.sql` (creates the database + 8 tables with proper
primary/foreign keys, `utf8mb4` charset for the accented Portuguese text) and
bulk-loads all 8 processed CSVs in dependency order.

Then apply the analytical views:

```bash
mysql -h 127.0.0.1 -P 3308 -u root -p < sql/views.sql
```

### 5. Connect Tableau

See [docs/tableau_setup.md](docs/tableau_setup.md) for driver install and
step-by-step connection instructions. For the current recommended approach —
one unified data source built from the 8 base tables via Tableau
Relationships (not per-chart SQL views) — see
[docs/data_model.md](docs/data_model.md), which lets a single filter control
every chart on a dashboard at once.

## Analysis

See [reports/analysis_report.md](reports/analysis_report.md) for the full
written analysis — revenue trends, top categories, state-level performance,
payment mix, delivery/review performance, and recommendations.

## Key findings (summary)

- **R$15.7M** total revenue across **98,199** orders (Sep 2016 – Aug 2018),
  average order value **R$160.24** (revenue ÷ orders — not a naive average of
  line-item prices, which understates it).
- **Health Beauty**, **Bed Bath Table**, and **Watches Gifts** are the top
  revenue-driving categories.
- **São Paulo** alone drives ~38% of revenue and ~42% of orders, but has the
  lowest average order value among top states — Bahia and Goiás customers
  order less often but spend more per order.
- **92.1%** of orders are delivered on or before the estimated date; average
  delivery time is **12.4 days**.
- Average review score **4.09/5**; only **3.12%** of unique customers are
  repeat buyers.

## Dashboards

You can view the interactive dashboards directly on Tableau Public:
- **[E-Commerce Performance Overview](https://public.tableau.com/views/E-CommercePerformanceOverview_17844666542380/PerformanceOverview?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

Beyond the main overview dashboard, dedicated dashboards were built for:
- **[Customers](https://public.tableau.com/views/CustomerSummary_17844666993460/CustomerDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)** — lifetime value distribution, acquisition trend, geographic
  concentration, repeat vs. one-time customer split
- **[Products](https://public.tableau.com/views/ProductDashboard_17844667429100/ProductDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)** — price distribution, freight cost as % of price by category,
  average delivery days by category
- **[Sellers & Delivery](https://public.tableau.com/views/SellersandDeliveryOverview/SellersAndDeliveryDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)** — revenue/volume by seller state, on-time delivery
  rate by state, delivery time trend
- **Reviews & Satisfaction** — review score trend, review score by state,
  review score vs. delivery speed

All dashboards share the same unified data source, so a filter placed on one
chart can control every chart on that dashboard at once.
