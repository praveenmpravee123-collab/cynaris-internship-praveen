# Apache Superset – BI Dashboard

## 1. Project Overview

This project demonstrates data visualization and dashboard creation using Apache Superset.

A sample Sales dataset was created using SQLite and connected to Apache Superset to build an interactive BI dashboard.

## 2. Tools and Technologies

- Apache Superset
- Docker Desktop
- SQLite
- SQL
- Microsoft Edge

## 3. Database Details

- Database Name: SQLite Practice DB
- Schema: main
- Table Name: sales
- Total Records: 5

### Table Columns

- id
- product
- category
- quantity
- price
- sales_date

## 4. SQL Analysis

### Total Sales Revenue

```sql
SELECT SUM(quantity * price) AS total_sales
FROM sales;
```

Result: 150100

### Category-wise Sales Revenue

```sql
SELECT category,
       SUM(quantity * price) AS total_sales
FROM sales
GROUP BY category;
```

### Product-wise Sales Revenue

```sql
SELECT product,
       SUM(quantity * price) AS total_sales
FROM sales
GROUP BY product;
```

### Monthly Sales Revenue

```sql
SELECT strftime('%Y-%m', sales_date) AS month,
       SUM(quantity * price) AS monthly_sales
FROM sales
GROUP BY month;
```

## 5. Dashboard Charts

Five visualizations were created:

1. Category-wise Sales – Bar Chart
2. Monthly Sales Trend – Line Chart
3. Category Distribution – Pie Chart
4. Total Sales – Big Number
5. Sales Details Table – Table Chart

## 6. Dashboard

Dashboard Name: Superset Practice Dashboard

All five charts were added to the dashboard.

## 7. Evidence

Dashboard image: `evidence/superset_dashboard.jpg`

## 8. Conclusion

Successfully configured Apache Superset, connected a SQLite database, performed SQL analysis, created five visualizations, and exported the dashboard as an image.
