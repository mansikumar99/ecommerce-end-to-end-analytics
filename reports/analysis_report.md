# E-Commerce Business Analysis Report

This report mirrors exactly what is shown across the four Tableau dashboards: Performance Overview, Customer Dashboard, Product Dashboard, and Sellers and Delivery Dashboard. Each dashboard now includes interactive filters, listed under its section below.

## Data Overview 

The data comes from the Olist Brazilian E-Commerce dataset, which includes orders placed on the Olist marketplace between September 4, 2016, and October 17, 2018.

The dataset contains information about:

| Entity | Count |
| :--- | :--- |
| Customers | 99,440 |
| Orders | 99,440 |
| Products | 32,951 |
| Product Categories | 74 |
| Sellers | 3,095 |

The data is organized into several connected tables, including orders, customers, order items, payments, reviews, products, sellers, and location data. Since all of these tables are linked together, applying a filter on the dashboard updates all related charts and visuals automatically.

Using this data, four dashboards were created:
* **Performance Overview Dashboard** – Shows overall business performance, key metrics, and sales trends.
* **Customer Dashboard** – Shows customer behavior, purchasing patterns, and customer value.
* **Product Dashboard** – Shows product prices, delivery times, shipping costs, and category performance.
* **Sellers & Delivery Dashboard** – Shows seller performance and delivery efficiency.

## Executive Summary 

* The business made **R$15.84 million** in total sales from about 99,440 orders, with customers spending an average of R$159 per order. Sales grew quickly at the beginning, but over time the growth slowed down and monthly revenue has stayed around R$1.0M–R$1.16M.
* The biggest challenge is **customer retention**. Almost 97% of customers only buy once, while only 3% come back to make another purchase. Since sales growth has slowed, encouraging existing customers to buy again could increase revenue more effectively than focusing only on finding new customers.
* Most of the business depends on **São Paulo**. It generates around 43% of the revenue among the top 10 states and around 70% of seller orders and seller revenue. This means the business relies heavily on one region, which could be risky.
* **Delivery performance is generally good.** Around 89% of orders are delivered on time, and most deliveries arrive within the fastest delivery time ranges. However, Office Furniture takes much longer to deliver than other popular product categories, making it an area that needs improvement.
* Customers mostly use **Credit Cards (78%) and Boleto (18%)** to pay, meaning over 96% of all payments come from these two payment methods. This shows that customers strongly prefer these payment options.

## 1. Performance Overview

**Filters available:** Customer City, Customer State, Customer Type, Order Date (range: 9/4/2016 - 10/17/2018), Order Status, Payment Type, Product Category, Seller City, Seller State.

### Headline Numbers

| Customers | Orders | Categories | Products Sold | Sellers | Order Total | Avg Order Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 99,440 | 99,440 | 74 | 32,951 | 3,095 | R$15.84M | R$159 |

**Insight:** The business has processed 99,440 orders from a near-equal count of customers, generating R$15.84M in total revenue at an average order value of R$159. Sellers (3,095) are far outnumbered by products (32,951) and categories (74), meaning each seller carries roughly 10-11 listed products on average.

### Revenue Over Time
**Insight:** Revenue growth is not linear - it climbs sharply through the first ~15 months (from near R$0.00M to R$1.18M, its peak), then flattens into a plateau, oscillating between roughly R$1.00M and R$1.16M for the remainder of the period. The business has moved from a growth phase into a steady-state phase.

### Payment Method
**Insight:** Credit Card is the dominant payment method by a wide margin (78.34%), with Boleto a distant second (17.92%). Voucher and Debit Card together account for under 4% of payments combined, making them a minor part of the payment mix.

### Revenue Over State (Top 10)
**Insight:** SP alone (R$5.92M) generates more revenue than the next four states combined (RJ + MG + RS + PR = R$5.68M), making it roughly 43% of the top-10 states' total revenue. Revenue is heavily concentrated in the Southeast region (SP, RJ, MG), with a long tail of smaller-revenue states.

### Orders by Day of Week
**Insight:** Order volume declines steadily from Monday (16,196, the highest) through the work week to Friday (14,122), then drops further on the weekend, with Saturday (10,887) the lowest day of the week. Weekday orders (Mon-Fri) account for roughly 77% of total orders, weekend orders for about 23%.

### Delivery Time Distribution
**Insight:** The first two delivery-time buckets together account for 82.63% of all orders, meaning the large majority of deliveries complete quickly. Only a small tail (buckets 4-6, roughly 7% combined) of orders fall into the slower delivery windows.

### Category Performance (Top 5)
**Insight:** The top 5 categories are fairly close in revenue, ranging from R$1.44M (Beleza Saude) down to R$1.06M (Informatica Acessorios) - a spread of only about 36% between the highest and lowest of the top 5. No single category dominates the way SP dominates by state.

## 2. Customer Dashboard

**Filters available:** Customer State, Customer Type, LTV Bucket, Order Date.

### Headline Numbers

| Total Customers | Avg Items per Order | Avg Order Value | Customer LTV |
| :--- | :--- | :--- | :--- |
| 99,441 | 1.13 | R$159 | R$15.84M |

**Insight:** With 99,441 total customers averaging just 1.13 items per order, purchasing behavior is dominated by small, single-item transactions rather than large basket orders.

### Customer Type
**Insight:** The overwhelming majority of customers (96.88%) buy only once; just 3.12% return for a second order or more. Repeat purchasing is a very small share of the customer base.

### Customers by City (Top 10)
**Insight:** Sao Paulo (14,984 customers) has more than double the customer count of the next-largest city, Rio De Janeiro (6,620) - a similar concentration pattern to what's seen in the state-level revenue data. Belo Horizonte and Brasilia are a clear second tier (around 2,000-2,700 customers each), with the remaining cities in the top 10 trailing further behind.

### Customer Lifetime Value Distribution
**Insight:** Customer lifetime value clusters heavily in the two middle buckets, which together hold 62.07% of all customers. Both the lowest and highest LTV buckets are minority segments (16.95% and 5.04% respectively), so extreme low-value and high-value customers are the exception, not the rule.

## 3. Product Dashboard

**Filters available:** Order Date, Price Bucket, Order Status.

### Headline Numbers

| Avg. Price | Avg. Review Score | Categories | Products Sold |
| :--- | :--- | :--- | :--- |
| R$120.65 | 4.1 | 74 | 32,951 |

**Insight:** With an average price of R$120.65 and average review score of 4.1 out of 5, the catalog sits at a moderate price point with generally positive customer satisfaction. 74 categories cover 32,951 distinct products, an average of roughly 445 products per category.

### Price Distribution
**Insight:** Over 62% of products sold (Bucket R$0-50 + R$50-100 combined) fall under R$100, and the share shrinks steadily at each higher price tier - only 4.65% of products sell for R$500 or more. The catalog is weighted toward lower-priced items.

### Avg Delivery Days by Category (Top 10)
**Insight:** Office Furniture takes noticeably longer to deliver (20.6 days) than every other category in the top 10, which cluster more tightly in the 13.8-15.7 day range. Categories associated with larger or bulkier items (Office Furniture, Fashion Shoes) lead this list.

### Freight % by Category (Top 10)
**Insight:** Home Comfort 2 stands out with freight costs equal to 54% of the item's price, and Flowers is close behind at 44% - both far above the rest of the top 10, which sit in the 27-37% range. For these categories, shipping is a very large proportion of what the customer pays.

## 4. Sellers And Delivery Dashboard

**Filters available:** Order Date, Seller City, Delivery Bucket.

### Headline Numbers

| Avg Revenue per Seller | Delivered on Time % | Avg. Delivery Days | Sellers |
| :--- | :--- | :--- | :--- |
| R$5,119 | 89.2% | 12.5 | 3,095 |

**Insight:** With 3,095 sellers generating R$5,119 average revenue each, and an 89.2% on-time delivery rate at an average of 12.5 days, overall fulfillment performance is strong across the seller base.

### Order Volume by Seller State
**Insight:** Seller order volume is extremely concentrated: SP alone (70,188 orders) accounts for roughly 70% of all seller-attributed order volume, more than nine times the next-highest state, MG (7,930). The remaining states form a long, rapidly shrinking tail down to single-digit order counts in states like AM (3) and AC (1).

### On-Time Delivery Rate by State (Top 5)
**Insight:** The states with the highest on-time delivery rates (AC, AP, AM, RO - all above 93%) are not the same states that drive the most order volume or revenue; SP, the volume leader, doesn't appear in this top-5 on-time list at all. High delivery reliability here comes from lower-volume states.

### Revenue by Seller State (Top 5)
**Insight:** SP sellers generate R$10.24M of the top-5 states' combined R$14.60M - about 70% of that total, mirroring the same concentration seen in order volume. PR, MG, RJ, and SC each contribute under R$1.5M, a fraction of SP's share.

## Recommendations

* **Retention is the biggest opportunity.** Only 3.12% of customers are repeat buyers (96.88% are one-time). Since revenue growth has already plateaued (Section 1), converting even a small share of the one-time customer base into repeat buyers would be a more direct growth lever than acquiring new customers.
* **Reduce geographic concentration risk.** SP accounts for roughly 43% of top-10 state revenue, ~70% of seller order volume, and ~70% of seller revenue. This dependence on a single state means any disruption there (logistics, demand, competition) would have an outsized impact on the whole business; expanding seller and customer presence in the next-tier states (RJ, MG, PR) would reduce this exposure.
* **Address freight costs on specific categories.** Home Comfort 2 (54%) and Flowers (44%) have freight costs that are a disproportionate share of the item price compared to the rest of the top 10 (27-37%). Reviewing packaging, carrier rates, or pricing for these two categories specifically could improve their margins.
* **Investigate Office Furniture's delivery time.** At 20.6 days, it takes meaningfully longer to deliver than every other top-10 category (13.8-15.7 days). Given delivery speed is otherwise strong (89.2% on-time overall), this category is a clear outlier worth a closer look.
* **Payment method diversification is low-risk to simplify.** Credit Card and Boleto together cover over 96% of payment volume; Voucher and Debit Card are marginal. This isn't necessarily a problem, but it means any checkout or payment-experience investment should prioritize those two primary methods first.
