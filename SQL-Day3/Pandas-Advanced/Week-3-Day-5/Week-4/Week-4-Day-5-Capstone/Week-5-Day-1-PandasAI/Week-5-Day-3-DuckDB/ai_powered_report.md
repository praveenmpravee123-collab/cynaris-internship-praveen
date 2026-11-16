# AI-Powered EDA on Indian Job Market Dataset

## 1. Project Overview

This project explores the Indian job market dataset using Python, PandasAI, and a locally hosted LLM through Ollama.

## 2. Dataset Information

- Dataset: job_market_india_100k.csv
- Original records: 100,000
- Cleaned records: 830
- Columns: 6

## 3. Tools and Technologies

- Python
- Pandas
- PandasAI 3.0.0
- Ollama
- Llama 3.2 3B
- Matplotlib
- Seaborn

## 4. Key Findings

1. Delivery Partner/Delivery Executive is the most frequent job title.
2. Uttar Pradesh has the highest average monthly salary in the analyzed data.
3. Final Monthly Salary contains 243 missing values.
4. HR Trainee has the highest average salary among job titles with at least 2 records (₹142,000), based on only 2 records.

## 5. PandasAI Results

- Top 5 job titles: Successful.
- Average salary by state: Successful.
- Missing values analysis: Incorrect AI response; verified using Python.
- Top-paying job titles: SQL validation failed; verified using Python.

## 6. Limitations

- The local Llama 3.2 3B model did not consistently generate SQL code compatible with PandasAI v3.
- Some AI-generated results required independent Python verification.
- Salary comparisons may be affected by small sample sizes.
- Exact duplicate removal reduced the dataset from 100,000 rows to 830 unique rows.

## 7. Conclusion

The project demonstrates how PandasAI and a locally hosted LLM can support exploratory data analysis. AI-generated results were cross-checked with Python to improve reliability.
