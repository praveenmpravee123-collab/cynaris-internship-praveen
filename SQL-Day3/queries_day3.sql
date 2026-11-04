-- SQL Aggregations - Week 1 Day 3


-- 1. COUNT
SELECT COUNT(*) AS total_sales
FROM sales;


-- 2. SUM
SELECT SUM(revenue) AS total_revenue
FROM sales;


-- 3. AVG
SELECT AVG(revenue) AS average_revenue
FROM sales;


-- 4. MAX
SELECT MAX(revenue) AS highest_revenue
FROM sales;


-- 5. MIN
SELECT MIN(revenue) AS lowest_revenue
FROM sales;


-- 6. GROUP BY city with SUM
SELECT city, SUM(revenue) AS total_revenue
FROM sales
GROUP BY city;


-- 7. GROUP BY category with AVG
SELECT category, AVG(revenue) AS average_revenue
FROM sales
GROUP BY category;


-- 8. GROUP BY city with HAVING
SELECT city, SUM(revenue) AS total_revenue
FROM sales
GROUP BY city
HAVING SUM(revenue) > 10000;


-- 9. WINDOW FUNCTION
SELECT
    city,
    revenue,
    SUM(revenue) OVER() AS total_revenue
FROM sales;