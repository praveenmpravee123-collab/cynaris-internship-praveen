# W8D1 – CIA Full Feature Integration Report

## 1. Project Overview

**Project:** Conversational Insights Automation (CIA)  
**Internship:** Data Analyst Internship – Cynaris Solutions  
**Task:** Executive Summary Generation and Full API Integration  
**Status:** Completed – Functional Testing

## 2. Objective

Integrate CSV upload, exploratory data analysis (EDA),
natural language querying, Groq AI executive summary
generation, and PowerPoint export into one FastAPI application.

## 3. Technology Stack

- Python
- FastAPI and Uvicorn
- Pandas
- PandasAI
- Ollama (qwen2.5:3b)
- Groq (openai/gpt-oss-20b)
- python-pptx
- Swagger UI

## 4. Dataset Overview

Dataset: CRM Customer Data

- Total Records: 100
- Total Columns: 10
- Missing Values: 0
- Duplicate Records: 0
- Total Deal Value: INR 24,875,000
- Average Deal Value: INR 248,750

## 5. API Endpoints

| Method | Endpoint               | Purpose                                  |
| ------ | ---------------------- | ---------------------------------------- |
| GET    | /                      | API Health Check                         |
| POST   | /cia/upload-csv        | Upload and validate CRM CSV              |
| GET    | /cia/eda               | Generate EDA statistics and insights     |
| POST   | /cia/query             | Natural language querying using PandasAI |
| POST   | /cia/executive-summary | Generate executive summary using Groq    |
| POST   | /cia/export-ppt        | Export CRM executive report as PPTX      |

## 6. EDA Findings

### Sales Pipeline Distribution

| Stage       | Records |
| ----------- | ------: |
| Qualified   |      28 |
| Won         |      22 |
| Proposal    |      15 |
| New Lead    |      14 |
| Negotiation |      11 |
| Lost        |      10 |

These values represent current pipeline stages,
not historical conversion rates.

### Top Sales Representatives

| Sales Representative | Total Deal Value (INR) |
| -------------------- | ---------------------: |
| Rahul Menon          |              5,215,000 |
| Karthik Nair         |              4,840,000 |
| Priya Shah           |              4,830,000 |

The top three representatives contribute
approximately 59.8% of the total recorded deal value.

## 7. AI Integration

PandasAI was integrated with the local Ollama
qwen2.5:3b model for natural language data queries.

Groq was integrated using the openai/gpt-oss-20b
model for executive summary generation.

The Groq API key is loaded from an environment file
and is not hardcoded in the application.

The generated AI summary was tested successfully.
Some AI-generated percentage claims required manual
validation against the source data.

## 8. PowerPoint Export

The PowerPoint export endpoint generates a
seven-slide executive report containing:

1. Project Title
2. Executive Summary
3. Key CRM Metrics
4. Sales Pipeline Distribution Chart
5. Sales Representative Performance Chart
6. Top Sales Insights
7. Business Recommendations

The exported presentation uses validated EDA
metrics rather than inserting the Groq-generated
summary directly.

Output: CIA_CRM_Executive_Report.pptx

## 9. Testing Results

| Test                            | Result |
| ------------------------------- | ------ |
| CSV Upload                      | Passed |
| EDA Generation                  | Passed |
| PandasAI Natural Language Query | Passed |
| Groq Executive Summary          | Passed |
| PowerPoint Export               | Passed |
| Seven-Slide Report Verification | Passed |

## 10. Evidence

Screenshots are stored in the evidence folder:

- 01_swagger_all_endpoints.png
- 02_groq_summary_success.png
- 03_eda_success.png
- 04_pandasai_query_success.png
- 05_ppt_export_success.png

## 11. Conclusion

The CIA application successfully integrates CSV
upload, EDA, natural language analytics, AI-based
executive summary generation, and PowerPoint export.

All primary endpoints were successfully tested
using Swagger UI and the CRM dataset.

The implementation demonstrates an end-to-end
analytics and executive reporting workflow.
