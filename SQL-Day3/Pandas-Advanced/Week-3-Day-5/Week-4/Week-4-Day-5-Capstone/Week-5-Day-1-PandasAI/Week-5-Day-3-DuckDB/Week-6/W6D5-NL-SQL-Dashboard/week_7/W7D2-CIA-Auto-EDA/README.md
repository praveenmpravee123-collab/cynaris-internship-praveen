# W7D2 – CIA Auto EDA: ydata-profiling + SweetViz Integration

## Project Overview

This project performs automated Exploratory Data Analysis (EDA) on an Indian Job Market dataset using AutoViz and SweetViz.

The objective is to generate automated visualizations, identify important dataset patterns, compare both EDA tools, and recommend a suitable tool for business stakeholders.

## Dataset Information

- Dataset: job_market_india.csv
- Total Records: 835
- Total Columns: 6
- Duplicate Records: 5

### Dataset Features

1. Job Title
2. Location
3. Salary
4. Monthly Salary
5. Locality
6. State

## Tools and Libraries

- Python 3.11.9
- Pandas
- NumPy
- Matplotlib
- Seaborn
- AutoViz
- SweetViz

## Tasks Completed

### 1. AutoViz Analysis

- Generated automated visualizations.
- Analyzed numerical and categorical variables.
- Exported interactive HTML charts.

Generated files:

- cat_var_plots.html
- distplots_nums.html
- violinplots.html

### 2. SweetViz Analysis

- Generated a comprehensive HTML EDA report.
- Analyzed all six dataset features.
- Examined missing values, unique values, distributions, and statistical summaries.

Generated report:

- W7D2_SweetViz_Report.html

### 3. Key Observations

- Job Title: 709 distinct job titles.
- Location: Remote was the most frequent location with 89 records.
- Salary: 237 records (28%) had salary marked as Not specified.
- Monthly Salary: 497 available values and 338 missing values.
- Locality: 581 missing values (70%).
- State: 29 distinct categories, with Kerala being the most frequent.

### 4. AutoViz vs SweetViz Comparison

AutoViz provides interactive visualizations such as distribution plots, violin plots, and categorical charts.

SweetViz generates a structured HTML report containing dataset summaries, missing values, feature distributions, and associations.

Both tools are useful for automated EDA and complement each other in understanding dataset quality and patterns.

### 5. Business Stakeholder Recommendation

SweetViz is recommended for business stakeholders because it provides a comprehensive and structured HTML report. It makes dataset summaries, missing values, and feature distributions easier to review and communicate.

AutoViz is useful for analysts who need quick interactive visual exploration.

## Project Structure

```text
W7D2-CIA-Auto-EDA/
│
├── evidence/
│   ├── 01_autoviz_distribution.png
│   ├── 02_sweetviz_report_overview.png
│   └── 03_sweetviz_report_remaining.png
│
├── W7D2_AutoViz_Charts/
│   ├── cat_var_plots.html
│   ├── distplots_nums.html
│   └── violinplots.html
│
├── job_market_india.csv
├── w7d2_auto_eda.ipynb
├── W7D2_SweetViz_Report.html
└── README.md
```

## Conclusion

Successfully completed automated EDA using AutoViz and SweetViz. Generated interactive visualizations and a comprehensive HTML report, identified important dataset characteristics, and documented recommendations for business stakeholders.
