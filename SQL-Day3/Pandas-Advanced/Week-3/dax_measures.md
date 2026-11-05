# Week 3 — Day 2: DAX Basics

## 1. Total Sales Measure

```dax
Total Sales = SUM(Sales[SalesAmount])
```

**Explanation:** Calculates total sales based on the current filter context.

## 2. South Sales Measure

```dax
South Sales =
CALCULATE(
    [Total Sales],
    Sales[Region] = "South"
)
```

**Explanation:** Calculates total sales only for the South region using `CALCULATE()`.

## 3. Year-to-Date Sales Measure

```dax
YTD Sales =
TOTALYTD(
    [Total Sales],
    'Calendar'[Date]
)
```

**Explanation:** Calculates sales from the beginning of the year through the current date context.

## 4. Running Total Measure

```dax
Running Total =
VAR CurrentDate = MAX(Sales[Sale Date])
RETURN
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Sales[Sale Date]),
        Sales[Sale Date] <= CurrentDate
    )
)
```

**Explanation:** Calculates cumulative sales up to the current sale date.

## 5. Profit Margin Calculated Column

```dax
Profit Margin % =
DIVIDE(
    Sales[Profit],
    Sales[SalesAmount],
    0
) * 100
```

**Explanation:** Calculates profit margin as a percentage of sales and handles division by zero safely.

## Row Context vs Filter Context

- **Row context:** Calculates an expression for the current row, such as profit for each product.
- **Filter context:** Determines which rows are included in a calculation, such as sales for the South region.

## Summary

- Measures calculate results dynamically based on filter context.
- Calculated columns calculate values row by row.
- `CALCULATE()` modifies filter context.
- `TOTALYTD()` calculates year-to-date sales.
- Running totals calculate cumulative values over time.
