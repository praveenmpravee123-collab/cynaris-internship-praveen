# Week 6 Day 4 – Vanna + Superset Executive Reporting

## Project Overview

This project integrates Vanna AI with a SQLite sales database and Apache Superset to support natural-language sales analysis and executive reporting.

## Tools and Technologies

- Python 3.11
- Vanna AI
- Ollama (qwen2.5:3b)
- SQLite
- FastAPI
- Uvicorn
- Apache Superset
- SQL

## Database Details

- Database: `practice.db`
- Table: `sales`
- Columns: `id`, `product`, `category`, `quantity`, `price`, `sales_date`

## Vanna AI Integration

- Configured Vanna Agent with Ollama LLM.
- Registered the SQL execution tool.
- Added database schema instructions.
- Stored five natural-language-to-SQL training examples.
- Tested natural-language sales questions through the agent.

## FastAPI Integration

Created a FastAPI application to expose the Vanna sales assistant through an API.

Endpoint:

- `GET /` – API status
- `GET /health` – Health check
- `POST /ask` – Submit a sales question and receive Vanna results

## Sales Analysis Results

### Total Sales Revenue

₹150,100

### Category-wise Revenue

| Category    |  Revenue |
| ----------- | -------: |
| Accessories |  ₹16,100 |
| Electronics | ₹134,000 |

### Monthly Revenue

| Month         |  Revenue |
| ------------- | -------: |
| January 2026  | ₹112,500 |
| February 2026 |  ₹27,600 |
| March 2026    |  ₹10,000 |

## Superset Executive Dashboard

Created and updated the following dashboard charts:

- Total Sales
- Category-wise Sales
- Monthly Sales Trend
- Category Distribution
- Sales Details Table

Updated revenue metrics to use:

`SUM(quantity * price)`

## Evidence

Screenshots are available in the `evidence` folder:

1. Total revenue API test
2. Category revenue API test
3. Monthly revenue API test
4. Final executive dashboard

## Conclusion

Successfully tested Vanna AI natural-language sales queries through FastAPI and configured Apache Superset visualizations to calculate sales revenue using quantity multiplied by price.
