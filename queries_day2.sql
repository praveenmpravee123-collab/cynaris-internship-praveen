-- SQL Joins - Week 1 Day 2

-- 1. INNER JOIN
SELECT *
FROM employee e
INNER JOIN department d
ON e.emp_id = d.emp_id;


-- 2. LEFT JOIN
SELECT *
FROM employee e
LEFT JOIN department d
ON e.emp_id = d.emp_id;


-- 3. RIGHT JOIN
SELECT *
FROM employee e
RIGHT JOIN department d
ON e.emp_id = d.emp_id;


-- 4. FULL OUTER JOIN
SELECT *
FROM employee e
FULL OUTER JOIN department d
ON e.emp_id = d.emp_id;


-- 5. SELF JOIN
SELECT
    e1.emp_name AS employee1,
    e2.emp_name AS employee2,
    e1.emp_address
FROM employee e1
JOIN employee e2
ON e1.emp_address = e2.emp_address
AND e1.emp_id < e2.emp_id;


-- 6. Duplicate rows - using DISTINCT
SELECT DISTINCT
    e.emp_id,
    e.emp_name,
    e.emp_address
FROM employee e
INNER JOIN department d
ON e.emp_id = d.emp_id;