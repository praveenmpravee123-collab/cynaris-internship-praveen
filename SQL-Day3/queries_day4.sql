
-- Day 4: SQL Subqueries & CTEs
-- Task 1: Above-average sales

SELECT *
FROM employee
WHERE amount > (
    SELECT AVG(amount)
    FROM employee
);

-- Task 2: Top performer per region

SELECT *
FROM employee e
WHERE amount = (
    SELECT MAX(amount)
    FROM employee
    WHERE region = e.region
);

-- Task 3: Rewrite subquery using a CTE

WITH AverageSales AS (
    SELECT AVG(amount) AS avg_amount
    FROM employee
)
SELECT *
FROM employee
WHERE amount > (
    SELECT avg_amount
    FROM AverageSales
);

-- Task 4: Chain two CTEs

WITH RegionSales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM employee
    GROUP BY region
),
HighSales AS (
    SELECT region, total_sales
    FROM RegionSales
    WHERE total_sales > 25000
)
SELECT *
FROM HighSales;
