# Supermarket Data Quality Scorecard

## 1. Dataset Overview

- Dataset: SuperMarket Analysis
- Total rows: 1,000
- Total columns: 17
- Period covered: 1 January 2019 – 30 March 2019

## 2. Data Quality Assessment

| Dimension    | Assessment                                                         | Status             |
| ------------ | ------------------------------------------------------------------ | ------------------ |
| Completeness | No missing values found across 17 columns                          | Pass               |
| Accuracy     | Cannot fully verify without trusted source records                 | Needs verification |
| Consistency  | Sales calculation matched the expected formula for all rows        | Pass               |
| Timeliness   | Historical data; refresh schedule is unknown                       | Needs verification |
| Uniqueness   | No duplicate rows or Invoice IDs found                             | Pass               |
| Validity     | Tested quantity, price, sales, rating, dates and categories passed | Pass               |

## 3. Automated Validation

- Great Expectations checks defined: 8
- Original dataset: All 8 checks passed
- Test dataset: 3 injected errors detected
- Detected issues: Missing Invoice ID, duplicate Invoice ID and invalid Quantity

## 4. PII and Classification

- No obvious direct personal identifiers were found in the available column names.
- Invoice IDs should be handled as internal business identifiers.
- Confirm the organisation's data classification policy before sharing the dataset.

## 5. Improvement Recommendations

1. Validate data types and required fields during ingestion.
2. Enforce unique Invoice IDs.
3. Reject zero or negative quantities and prices.
4. Verify sales calculations automatically.
5. Define a data freshness SLA with the data producer.
6. Compare sampled records against trusted source transactions to assess accuracy.

## Conclusion

The dataset passed the eight defined checks before errors were injected.
The test confirmed that the validation rules detect three intentionally
introduced quality issues. Accuracy and timeliness require additional
business context for full assessment.
