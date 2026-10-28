CREATE TABLE sales (
    sales_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    revenue REAL,
    city TEXT
);
INSERT INTO sales VALUES
(1, 'arun', 'laptop', 'electronics', 1, 55000, 'bengaluru'),
(2, 'priya', 'mouse', 'electronics', 3, 1500, 'chennai'),
(3, 'karthik', 'keyboard', 'electronics', 2, 2400, 'bengaluru'),
(4, 'divya', 'office chair', 'furniture', 1, 8500, 'hyderabad'),
(5, 'rahul', 'monitor', 'electronics', 2, 30000, 'bengaluru'),
(6, 'sneha', 'desk', 'furniture', 1, 12000, 'chennai'),
(7, 'vijay', 'laptop bag', 'accessories', 2, 3000, 'mumbai'),
(8, 'anitha', 'headphone', 'electronics', 1, 4500, 'bengaluru'),
(9, 'suresh', 'webcam', 'electronics', 2, 7000, 'hyderabad'),
(10, 'ramesh', 'laptop', 'electronics', 1, 60000, 'hyderabad');
-- Query 1: Select all sales data
SELECT *
FROM sales;


-- Query 2: Select specific columns
SELECT customer_name, product, revenue
FROM sales;


-- Query 3: Sales with revenue greater than 10000
SELECT *
FROM sales
WHERE revenue > 10000;


-- Query 4: Bengaluru sales with revenue greater than 5000
SELECT *
FROM sales
WHERE revenue > 5000
  AND city = 'bengaluru';


-- Query 5: Sales from Bengaluru or Chennai
SELECT *
FROM sales
WHERE city = 'bengaluru'
   OR city = 'chennai';


-- Query 6: Sales excluding electronics
SELECT *
FROM sales
WHERE NOT category = 'electronics';


-- Query 7: Customers whose name starts with A
SELECT *
FROM sales
WHERE customer_name LIKE 'a%';


-- Query 8: Sales from selected cities
SELECT *
FROM sales
WHERE city IN ('bengaluru', 'chennai', 'mumbai');


-- Query 9: Sales with revenue between 3000 and 15000
SELECT *
FROM sales
WHERE revenue BETWEEN 3000 AND 15000;


-- Query 10: Sales where city is NULL
SELECT *
FROM sales
WHERE city IS NULL;