# W8D5 – AI Data Platform: Final Demo and Documentation

## 1. Project Overview

Conversational Insights Automation (CIA) is an AI-powered
data analytics platform that enables users to upload CRM
datasets, explore interactive dashboards, ask natural
language questions, generate automated EDA reports,
create executive summaries, and export PowerPoint reports.

This project represents the final integration, testing,
documentation, and demonstration of the Week 8 AI Data
Platform.

## 2. Project Objectives

- Build an integrated AI-powered analytics platform.
- Enable natural language data exploration.
- Automate exploratory data analysis.
- Generate business insights and recommendations.
- Export professional PowerPoint reports.
- Validate API functionality and security.
- Prepare the application for cloud deployment.
- Demonstrate the complete application workflow.

## 3. Technology Stack

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python 3.11.9         | Backend development          |
| FastAPI               | REST API development         |
| Uvicorn               | Application server           |
| Pandas                | Data processing and analysis |
| NumPy                 | Numerical operations         |
| PandasAI              | Natural language analytics   |
| Ollama                | Local LLM execution          |
| Qwen 2.5 3B           | Local AI model               |
| Groq                  | Executive summary generation |
| HTML, CSS, JavaScript | Dashboard interface          |
| python-pptx           | PowerPoint report generation |
| Pytest                | Automated API testing        |
| Swagger UI            | API documentation            |
| Git and GitHub        | Version control              |

## 4. Application Architecture

```text
User
  |
  v
Interactive Dashboard
  |
  v
FastAPI Backend
  |
  +-- CSV Upload and Validation
  +-- Pandas Data Processing
  +-- PandasAI and Ollama
  +-- Automated EDA
  +-- Groq Executive Summary
  +-- PowerPoint Report Export
```

## 5. Project Structure

```text
W8D5-Final-Platform-Demo/
|
|-- csv_upload_api.py
|-- dashboard.html
|-- requirements.txt
|-- requirements-cloud.txt
|-- test_api.py
|-- test_results.txt
|-- README.md
|-- W8D5_Final_Platform_Demo.mp4
|-- .env.example
|-- .gitignore
|-- .python-version
```

## 6. Application Features

### 6.1 CSV Upload and Validation

- Upload CRM datasets in CSV format.
- Validate required columns.
- Detect invalid and negative deal values.
- Reject empty datasets.
- Enforce dataset size restrictions.
- Calculate initial CRM metrics.

### 6.2 Interactive Dashboard

- Total customer records.
- Total recorded deal value.
- Average deal value.
- Sales pipeline distribution.
- Sales representative performance.
- Interactive data visualizations.

### 6.3 Natural Language Analytics

The local application integrates PandasAI with Ollama
using the Qwen 2.5 3B model.

Example questions:

- How many customers are there?
- What is the total deal value?
- What is the average deal value?
- What is the minimum deal value?
- What is the maximum deal value?
- Show deal stage distribution.
- Show sales performance.

### 6.4 Automated EDA

The EDA module provides:

- Dataset dimensions.
- Column information.
- Missing value analysis.
- Duplicate record detection.
- Descriptive statistics.
- Sales pipeline insights.
- Sales representative performance.

### 6.5 AI Executive Summary

Groq generates business-oriented executive summaries
using validated dataset statistics.

The generated summary includes:

- Dataset overview.
- Key business metrics.
- Sales pipeline insights.
- Representative performance.
- Business recommendations.

### 6.6 PowerPoint Report Export

The application generates a seven-slide PowerPoint report:

1. Title Slide
2. Executive Summary
3. Key CRM Metrics
4. Sales Pipeline Distribution
5. Sales Representative Performance
6. Top Sales Insights
7. Business Recommendations

The report includes charts, validated metrics, and
executive summary speaker notes.

## 7. Installation and Setup

### Step 1: Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 2: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Ollama

Install Ollama and download the required model:

```powershell
ollama pull qwen2.5:3b
```

Ensure the Ollama service is running before starting
the application.

### Step 5: Configure Environment Variables

Create a local environment configuration file:

```powershell
Copy-Item .env.example .env
```

Configure the following variables:

```env
APP_ENV=local
OLLAMA_MODEL=ollama/qwen2.5:3b
OLLAMA_API_BASE=http://localhost:11434
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
DEMO_USERNAME=mentor
DEMO_PASSWORD=
```

Replace the placeholder Groq API key with a valid key.

Never commit actual API keys, passwords, or the
.env file to GitHub.

### Step 6: Start the Application

```powershell
python -m uvicorn csv_upload_api:app --host 127.0.0.1 --port 8002
```

### Step 7: Access the Application

- Dashboard: http://127.0.0.1:8002/dashboard
- Swagger UI: http://127.0.0.1:8002/docs
- OpenAPI Schema: http://127.0.0.1:8002/openapi.json
- Health Check: http://127.0.0.1:8002/healthz

## 8. API Documentation

| Method | Endpoint                 | Description                   |
| ------ | ------------------------ | ----------------------------- |
| GET    | /dashboard               | Dashboard interface           |
| GET    | /healthz                 | Application health check      |
| GET    | /docs                    | Swagger API documentation     |
| GET    | /openapi.json            | OpenAPI schema                |
| POST   | /cia/upload-csv          | Upload and validate CSV       |
| POST   | /cia/query               | Natural language analytics    |
| GET    | /cia/supported-questions | Supported analytics questions |
| GET    | /cia/eda                 | Generate EDA results          |
| POST   | /cia/executive-summary   | Generate AI summary           |
| POST   | /cia/export-ppt          | Export PowerPoint report      |

## 9. Dataset Information

The application was validated using crm_data.csv,
a CRM dataset containing 100 records and 10 columns.

The dataset contains customer information, sales
representative details, deal values, and pipeline stages.

### Dataset Quality

- Total records: 100
- Total columns: 10
- Missing values: 0
- Duplicate records: 0

## 10. Validated Analytics Results

### Key Performance Indicators

| Metric             |          Value |
| ------------------ | -------------: |
| Total Records      |            100 |
| Total Columns      |             10 |
| Missing Values     |              0 |
| Duplicate Records  |              0 |
| Total Deal Value   | INR 24,875,000 |
| Average Deal Value |    INR 248,750 |
| Median Deal Value  |    INR 237,500 |
| Minimum Deal Value |     INR 15,000 |
| Maximum Deal Value |    INR 500,000 |
| Standard Deviation |     137,553.25 |

### Sales Pipeline Distribution

| Deal Stage  | Count |
| ----------- | ----: |
| Qualified   |    28 |
| Won         |    22 |
| Proposal    |    15 |
| New Lead    |    14 |
| Negotiation |    11 |
| Lost        |    10 |
| Total       |   100 |

### Sales Representative Performance

| Sales Representative | Deal Value (INR) |
| -------------------- | ---------------: |
| Rahul Menon          |        5,215,000 |
| Karthik Nair         |        4,840,000 |
| Priya Shah           |        4,830,000 |
| Sneha Iyer           |        3,640,000 |
| Aditi Rao            |        3,485,000 |
| Arjun Das            |        2,865,000 |
| Total                |       24,875,000 |

The top three sales representatives contribute
approximately 59.84% of the total recorded deal value.

Recorded deal values should not be interpreted as
confirmed revenue.

## 11. Business Recommendations

- Review lost deals to identify recurring issues.
- Prioritize follow-ups for Proposal and Negotiation stages.
- Share effective practices from top-performing representatives.
- Monitor pipeline progression regularly.
- Maintain dataset quality through validation.
- Track historical stage transitions before calculating
  conversion rates.

## 12. Manual Feature Validation

All major application features were successfully
verified in the W8D5 project folder on November 27, 2026.

| Feature                | Status |
| ---------------------- | ------ |
| Application Startup    | PASS   |
| Dashboard Loading      | PASS   |
| CSV Upload             | PASS   |
| Interactive Charts     | PASS   |
| Natural Language Query | PASS   |
| Automated EDA          | PASS   |
| Groq Executive Summary | PASS   |
| PowerPoint Export      | PASS   |

### AI Query Validation

Question:

```text
What is the total deal value?
```

Expected result:

```text
24875000
```

Actual result:

```text
24875000
```

Validation status: PASS

### Executive Summary Validation

- Summary generated successfully.
- Business metrics verified during initial validation.
- Sales representative values verified.
- Business recommendations included.
- Summary generation successfully retested in W8D5.

### PowerPoint Validation

- PowerPoint generated successfully.
- Total slides: 7.
- Chart data verified during initial validation.
- Executive summary included.
- Speaker notes included.
- Business recommendations included.
- Export successfully retested in W8D5.

## 13. Automated API Testing

Run the automated test suite:

```powershell
python -m pytest test_api.py -v
```

Save testing evidence:

```powershell
python -m pytest test_api.py -v | Tee-Object -FilePath test_results.txt
```

### Final W8D5 Test Results

| Metric         | Result            |
| -------------- | ----------------- |
| Total Tests    | 23                |
| Passed         | 23                |
| Failed         | 0                 |
| Success Rate   | 100%              |
| Execution Time | 2.91 seconds      |
| Warnings       | 1                 |
| Test Date      | November 27, 2026 |
| Overall Status | PASS              |

### Test Coverage

| Test Category              | Tests Passed |
| -------------------------- | -----------: |
| Health Check               |            1 |
| Authentication             |            2 |
| Dashboard Access           |            1 |
| API Documentation          |            2 |
| CSV Validation             |            6 |
| Supported Questions        |            1 |
| Numeric Analytics Queries  |            5 |
| Distribution Queries       |            2 |
| Unsupported Query Handling |            1 |
| Automated EDA              |            1 |
| Cross-Origin Protection    |            1 |
| Total                      |           23 |

### Final Test Output

```text
======================== 23 passed, 1 warning in 2.91s ========================
```

Testing evidence is available in:

[test_results.txt](test_results.txt)

All 23 automated API tests passed successfully in
the W8D5 project directory.

Live Ollama queries, Groq summary generation, and
PowerPoint export were additionally verified through
manual application testing.

## 14. Troubleshooting

### Matplotlib Import Error

During initial natural language query testing,
Windows Application Control blocked a Matplotlib
DLL from loading.

This caused PandasAI query execution to fail.

Resolution steps:

1. Stopped the application server.
2. Verified Matplotlib version 3.7.5.
3. Confirmed that Matplotlib and pyplot imported successfully.
4. Restarted the application server.
5. Uploaded the CRM dataset again.
6. Retested the natural language query.

The query returned the expected result of 24,875,000.

Natural language query execution was also successfully
verified in the W8D5 application.

The underlying Windows policy issue may recur.

### Application Import Error

The application initially failed to start when the
Uvicorn command was executed from the repository
root directory.

Error:

```text
Error loading ASGI app.
Could not import module "csv_upload_api".
```

Resolution:

Navigated to the W8D5-Final-Platform-Demo directory
and restarted the application.

The application started successfully.

### Dependency Warning

The automated test suite reported one Starlette
deprecation warning related to httpx.

All 23 tests passed despite the warning.

The dependency warning remains a future maintenance item.

## 15. Security and Configuration

- Environment-based application configuration.
- HTTP Basic authentication for cloud mode.
- CSV file size restrictions.
- Required column validation.
- Invalid numeric value validation.
- Cross-origin request protection.
- Environment variables for sensitive credentials.
- Git ignore rules for local configuration files.
- Restricted predefined analytics queries in cloud mode.

### Data Upload Restrictions

- Maximum CSV file size: 5 MB.
- Maximum records: 100,000.
- Maximum columns: 100.
- Required columns: deal_stage, sales_rep, deal_value.

Sensitive credentials must not be included in
source code, documentation, or demo recordings.

## 16. Cloud Deployment

The application supports separate local and cloud modes.

For cloud deployment, configure the environment variables
on the hosting platform:

```env
APP_ENV=cloud
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
DEMO_USERNAME=mentor
DEMO_PASSWORD=your_secure_password
```

The cloud demo password must contain at least
16 characters.

Cloud dependencies:

```text
requirements-cloud.txt
```

Suggested cloud startup command:

```bash
uvicorn csv_upload_api:app --host 0.0.0.0 --port $PORT
```

### Deployment Status

| Component                    | Status                             |
| ---------------------------- | ---------------------------------- |
| Local Application Validation | Completed                          |
| W8D5 Application Retest      | Completed                          |
| Cloud Configuration          | Prepared                           |
| Railway Deployment           | Authentication issue pending       |
| Render Deployment            | Repository access approval pending |
| Production URL               | Not yet available                  |
| Live Production Validation   | Pending                            |

Local application URL:

http://127.0.0.1:8002/dashboard

The application is working successfully in the local
environment.

Public cloud deployment and live production
verification remain pending.

## 17. AI Tutor Review

Two AI Tutor review interactions were completed
before the final submission process.

### Interaction 1: Application Implementation Review

Reviewed areas:

- CSV validation.
- Natural language queries.
- Automated EDA.
- Groq executive summary.
- PowerPoint export.
- Application architecture.

Suggested improvements:

- Modular application architecture.
- Enhanced CSV preview and validation.
- Query history and autocomplete.
- Improved interactive EDA visualizations.
- Prompt optimization.
- Custom PowerPoint branding.
- User feedback collection.

Status: Completed.

### Interaction 2: Testing and Deployment Readiness

Reviewed areas:

- Automated testing strategy.
- Application security.
- Documentation quality.
- Cloud deployment readiness.

Suggested improvements:

- End-to-end browser testing.
- Performance and load testing.
- Dependency vulnerability scanning.
- Rate limiting.
- Structured logging and monitoring.
- Automated CI/CD pipelines.
- Persistent data storage.
- Improved authentication and authorization.

Status: Completed.

### Review Outcome

The AI Tutor provided recommendations for future
enhancements.

Some review statements assumed features that were
not verified in the current implementation.

Only implemented and validated features are
reported as completed in this documentation.

Additional recommendations are retained as future
improvements rather than claimed as completed work.

## 18. Final Demo Video

The final application demonstration was recorded
after successful local feature verification.

### Video Information

| Property           | Details                      |
| ------------------ | ---------------------------- |
| Filename           | W8D5_Final_Platform_Demo.mp4 |
| Format             | MP4                          |
| File Size          | 5.46 MB                      |
| Recording Status   | Completed                    |
| Compression Status | Completed                    |
| Environment        | Local                        |
| Recording Date     | November 27, 2026            |

### Demonstration Workflow

1. Application introduction.
2. CSV dataset upload.
3. Interactive dashboard and charts.
4. Natural language query execution.
5. Automated exploratory data analysis.
6. Groq executive summary generation.
7. PowerPoint report export.
8. Final application validation.

### Demo Video

[View Final Platform Demo](W8D5_Final_Platform_Demo.mp4)

The demonstration represents the working local
application, not a publicly deployed production instance.

## 19. Known Limitations

- Local natural language analytics requires Ollama.
- Executive summary generation requires a valid Groq API key.
- Cloud mode supports restricted predefined analytics queries.
- Uploaded dataset state is stored in application memory.
- Restarting the server requires uploading the dataset again.
- Local LLM responses may occasionally require retries.
- Windows Application Control may affect dependency loading.
- One dependency deprecation warning remains.
- Advanced load and security testing are not completed.
- Live cloud deployment and production verification are pending.

## 20. Future Improvements

- Complete cloud deployment and production validation.
- Implement persistent database storage.
- Add multi-user dataset isolation.
- Improve natural language query reliability.
- Introduce role-based access control.
- Implement API rate limiting.
- Add additional dataset formats.
- Implement structured logging and monitoring.
- Expand automated test coverage.
- Add end-to-end browser testing.
- Implement automated CI/CD pipelines.
- Introduce schema versioning.
- Add query history and autocomplete.
- Improve dashboard customization.
- Support custom PowerPoint branding.
- Add user feedback for AI-generated summaries.
- Implement dependency vulnerability scanning.

## 21. Final Completion Checklist

- [x] W8D5 project folder created.
- [x] Application files integrated.
- [x] Dashboard title updated.
- [x] Local application startup verified.
- [x] CSV upload verified.
- [x] Interactive dashboard verified.
- [x] Ollama natural language queries verified.
- [x] Automated EDA verified.
- [x] Groq executive summary verified.
- [x] PowerPoint export verified.
- [x] All 23 automated API tests passed.
- [x] Test evidence saved.
- [x] README documentation completed.
- [x] AI Tutor Interaction 1 completed.
- [x] AI Tutor Interaction 2 completed.
- [x] Final demo video recorded.
- [x] Demo video compressed to 5.46 MB.
- [ ] Git commits and push.
- [ ] Final pull request submission.
- [ ] Cloud deployment.
- [ ] Live production verification.

## 22. Deliverables

| Deliverable                    | Status       |
| ------------------------------ | ------------ |
| FastAPI Application            | Completed    |
| Interactive Dashboard          | Completed    |
| CSV Validation                 | Completed    |
| Ollama Integration             | Completed    |
| Automated EDA                  | Completed    |
| Groq Integration               | Completed    |
| PowerPoint Export              | Completed    |
| Automated API Tests            | 23/23 Passed |
| Testing Evidence               | Completed    |
| README Documentation           | Completed    |
| AI Tutor Reviews               | 2 Completed  |
| Final Demo Video               | Completed    |
| Cloud Deployment Configuration | Prepared     |
| Public Production Deployment   | Pending      |
| Final Pull Request             | Pending      |

### Evidence Files

- [Application Source Code](csv_upload_api.py)
- [Dashboard](dashboard.html)
- [Automated Test Suite](test_api.py)
- [Final Test Results](test_results.txt)
- [Final Demo Video](W8D5_Final_Platform_Demo.mp4)

## 23. Conclusion

The CIA AI Data Platform successfully integrates
data processing, interactive visualization, natural
language analytics, automated EDA, AI-generated
executive summaries, and PowerPoint report generation.

All major application features were successfully
verified in the W8D5 local environment.

The final automated API test suite achieved a
100% pass rate, with 23 tests passed, zero failures,
and one deprecation warning in 2.91 seconds.

Two AI Tutor review interactions were completed,
and the final application demonstration was recorded
and compressed to 5.46 MB.

Local implementation, testing, documentation,
and demonstration are completed.

Git submission, public cloud deployment, and
live production verification remain pending.

## 24. Author

Praveen Kumar M

Data Analyst Intern

Cynaris Solutions Pvt. Ltd.

Week 8 – Day 5

Date: November 27, 2026
