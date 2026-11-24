# Week 5 Day 2 - AutoViz & SweetViz

## Objective

Perform automated Exploratory Data Analysis (EDA) using AutoViz and SweetViz Python libraries.

## Dataset

- Dataset: job_market_india.csv
- Original records: 835
- Original columns: 6
- Cleaned records: 835
- Cleaned columns: 4
- Missing values after cleaning: 0

## Tools Used

- Python
- Pandas
- NumPy
- AutoViz
- SweetViz
- Matplotlib
- Seaborn

## Data Preparation

- Removed Salary and Locality columns.
- Filled missing Monthly Salary values using the median.
- Converted Job Title, Location, and State columns into categorical data types.

## AutoViz Reports

Generated the following HTML visualizations:

1. cat_var_plots.html
2. distplots_nums.html
3. violinplots.html

## SweetViz Report

Generated an interactive HTML report:

- sweetviz_report.html

## Key Insights

1. Median monthly salary: ₹19,250.
2. Mean monthly salary: ₹45,342.56.
3. The mean is higher than the median, indicating a right-skewed salary distribution.
4. Highest recorded monthly salary: ₹939,847.18.
5. Unusually high salary values should be validated.

## AutoViz vs SweetViz

- AutoViz is useful for quick automated visual exploration.
- SweetViz provides detailed statistics, distributions, missing-value analysis, and feature associations.
- Both tools reduce manual EDA effort.

## Business Stakeholder Recommendation

SweetViz is recommended because its interactive HTML report makes data insights easier to understand and communicate.

## Conclusion

Automated EDA using AutoViz and SweetViz helped explore salary distributions, identify patterns, and generate shareable HTML reports.
