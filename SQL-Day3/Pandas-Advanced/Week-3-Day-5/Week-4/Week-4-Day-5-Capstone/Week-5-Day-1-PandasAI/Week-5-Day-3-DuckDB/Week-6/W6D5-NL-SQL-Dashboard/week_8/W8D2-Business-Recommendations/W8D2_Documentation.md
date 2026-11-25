# W8D2 – Business Recommendations: AI Narrative from Analytics

## Objective

Generate AI-powered executive summaries and actionable business recommendations from analytical insights and export them as a PowerPoint report.

## Tools and Technologies

- Python
- Jupyter Notebook
- Pandas and NumPy
- Ollama – qwen2.5:3b
- Python-pptx
- Tkinter

## Dataset

- Dataset: job_market_india.csv
- Original records: 835
- Cleaned records: 830
- Duplicates removed: 5
- Usable salary records: 492

## Implementation

1. Implemented CSV selection using Tkinter.
2. Performed exploratory data analysis and data cleaning.
3. Standardized annual salaries into monthly salaries.
4. Generated five analytical insights.
5. Generated an AI executive summary and business recommendations.
6. Manually validated AI-generated content to remove unsupported claims.
7. Exported a seven-slide PowerPoint report with five individual insight charts.

## Key Findings

- Kerala recorded the highest number of job listings: 159.
- Delivery Partner/Delivery Executive was the most frequently listed job title.
- Average monthly salary: INR 22,850.86.
- Median monthly salary: INR 18,500.
- Remote opportunities: 10.72%.
- Missing usable salary information: 40.72%.

## AI Integration

Ollama with qwen2.5:3b was used as a local alternative to Groq, avoiding external API dependencies.

The final manually validated executive summary contains 192 words.

## Challenges and Solutions

- CSV upload widget rendering issue: resolved using Tkinter.
- Inconsistent salary periods: standardized annual salary values.
- Unsupported AI claims: corrected through manual validation.
- PowerPoint content overflow: resolved by restructuring the presentation.

## Validation Results

- CSV Loading: PASS
- Data Cleaning: PASS
- EDA and Insights: PASS
- Executive Summary: PASS
- Business Recommendations: PASS
- Seven-Slide PPT Export: PASS
- Five Individual Insight Charts: PASS
- Executive Summary Speaker Notes: PASS

## Deliverables

- w8d2_business_recommendations.ipynb
- W8D2_Business_Recommendations.pptx
- W8D2_Documentation.md

## Conclusion

Successfully implemented and validated a CSV-to-analytics-to-AI-report workflow with actionable business recommendations and PowerPoint export.
