# CIA - CRM Analytics Dashboard

## W8D4: Production Deployment and API Documentation

### 1. Project Overview

Conversational Insights Automation (CIA) is a CRM analytics
application that enables users to upload CSV datasets,
generate analytical insights, ask natural language questions,
visualize sales performance, generate AI-powered executive
summaries, and export PowerPoint reports.

The application supports both local and cloud deployment modes.

### 2. Features

- CSV dataset upload and validation
- Interactive CRM analytics dashboard
- Customer count and total deal value KPIs
- Deal stage distribution charts
- Sales representative performance charts
- Automated Exploratory Data Analysis (EDA)
- Natural language queries using PandasAI and Ollama locally
- Restricted analytics queries in cloud mode
- Groq-powered executive summary generation
- Seven-slide PowerPoint report generation
- Executive summary in PowerPoint speaker notes
- Swagger API documentation
- Password-protected cloud demo
- Environment-based configuration
- Health check endpoint
- Secure API error handling
- Automated API testing

### 3. Technology Stack

| Component            | Technology                        |
| -------------------- | --------------------------------- |
| Programming Language | Python 3.11.9                     |
| Backend              | FastAPI                           |
| API Server           | Uvicorn                           |
| Data Analysis        | Pandas, NumPy                     |
| Local AI             | PandasAI, Ollama                  |
| Local LLM            | qwen2.5:3b                        |
| Executive Summary    | Groq                              |
| Groq Model           | openai/gpt-oss-20b                |
| Frontend             | HTML, CSS, JavaScript             |
| Visualization        | Chart.js                          |
| Report Generation    | python-pptx                       |
| Configuration        | python-dotenv                     |
| Authentication       | HTTP Basic Authentication         |
| Testing              | Pytest, HTTPX, FastAPI TestClient |
| Deployment Platform  | Render (Planned)                  |
| Version Control      | Git and GitHub                    |

### 4. Project Structure

```text
W8D4-Production-Deployment/
├── csv_upload_api.py
├── dashboard.html
├── chart_data.json
├── requirements.txt
├── requirements-cloud.txt
├── .python-version
├── .env.example
├── .gitignore
├── test_api.py
├── test_results.txt
└── README.md
```

### 5. Local Setup Instructions

#### Step 1: Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Step 2: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

#### Step 3: Configure Ollama

Install Ollama and download the required model.

```powershell
ollama pull qwen2.5:3b
```

Ensure Ollama is running before starting the application.

#### Step 4: Configure Environment Variables

Create a `.env` file using `.env.example` as a template.

```env
APP_ENV=local
OLLAMA_MODEL=ollama/qwen2.5:3b
OLLAMA_API_BASE=http://localhost:11434
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit actual API keys or passwords to GitHub.

#### Step 5: Start the Application

```powershell
python -m uvicorn csv_upload_api:app --host 127.0.0.1 --port 8002
```

#### Step 6: Access the Application

- API: http://127.0.0.1:8002
- Dashboard: http://127.0.0.1:8002/dashboard
- Swagger UI: http://127.0.0.1:8002/docs
- Health Check: http://127.0.0.1:8002/healthz

### 6. Dataset Requirements

The application accepts CSV files containing at least
the following columns:

- deal_stage
- sales_rep
- deal_value

Validation rules:

- Maximum file size: 5 MB
- Maximum rows: 100,000
- Maximum columns: 100
- Required columns must be present
- Deal values must be finite numeric values
- Negative deal values are rejected
- Sales representative and deal stage values cannot be missing

Only synthetic or authorized sample datasets should be
used for cloud demonstrations.

### 7. API Documentation

| Method | Endpoint                 | Description                |
| ------ | ------------------------ | -------------------------- |
| GET    | /                        | API status                 |
| GET    | /healthz                 | Health check               |
| GET    | /dashboard               | CRM dashboard              |
| GET    | /docs                    | Swagger documentation      |
| GET    | /openapi.json            | OpenAPI schema             |
| GET    | /chart_data.json         | Local sample chart data    |
| POST   | /cia/upload-csv          | Upload CRM dataset         |
| GET    | /cia/eda                 | Generate EDA               |
| POST   | /cia/query               | Execute analytics query    |
| GET    | /cia/supported-questions | Supported cloud questions  |
| POST   | /cia/executive-summary   | Generate AI summary        |
| POST   | /cia/export-ppt          | Download PowerPoint report |

#### Example Query Request

```json
{
  "question": "What is the total deal value?"
}
```

For the 100-record demonstration dataset, the expected
total deal value is INR 24,875,000.

### 8. Application Workflow

1. Open the CRM analytics dashboard.
2. Upload a valid CRM CSV dataset.
3. View customer count and total deal value.
4. Explore deal stage and sales performance charts.
5. Submit an analytics question.
6. Generate the EDA report.
7. Generate the Groq executive summary.
8. Export the PowerPoint report.

### 9. Local and Cloud Modes

#### Local Mode

- Uses PandasAI and Ollama for natural language queries.
- Uses Groq for executive summary generation.
- Runs on the local machine.
- Intended for trusted local users.

#### Cloud Mode

- Does not require Ollama or PandasAI.
- Uses predefined analytics queries.
- Uses Groq for executive summary generation.
- Requires password authentication.
- Intended for a single-user demonstration.
- Rejects unsupported analytics questions.
- Disables access to static sample chart data.

### 10. Supported Cloud Queries

1. How many customers are there?
2. What is the total deal value?
3. What is the average deal value?
4. What is the minimum deal value?
5. What is the maximum deal value?
6. Show deal stage distribution
7. Show sales performance

### 11. Cloud Deployment Configuration

Planned deployment platform: Render Free Web Service.

Python version:

```text
3.11.9
```

Root directory:

```text
SQL-Day3/Pandas-Advanced/Week-3-Day-5/Week-4/Week-4-Day-5-Capstone/Week-5-Day-1-PandasAI/Week-5-Day-3-DuckDB/Week-6/W6D5-NL-SQL-Dashboard/week_8/W8D4-Production-Deployment
```

Build command:

```bash
pip install -r requirements-cloud.txt
```

Start command:

```bash
python -m uvicorn csv_upload_api:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/healthz
```

Required environment variables:

```env
APP_ENV=cloud
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
DEMO_USERNAME=mentor
DEMO_PASSWORD=your_secure_password
```

The cloud password must contain at least 16 characters.
Use a unique password and configure secrets directly
in the hosting platform.

Use HTTPS for the deployed application.

### 12. Testing and Validation

#### Local Mode Testing

| Test Case                         | Result |
| --------------------------------- | ------ |
| API startup                       | PASS   |
| Dashboard loading                 | PASS   |
| CSV upload                        | PASS   |
| PandasAI and Ollama query         | PASS   |
| EDA generation                    | PASS   |
| Groq executive summary generation | PASS   |
| PowerPoint export                 | PASS   |
| Swagger documentation loading     | PASS   |

#### Cloud Mode Testing on Local Machine

| Test Case                               | Result  |
| --------------------------------------- | ------- |
| Cloud mode startup                      | PASS    |
| Authenticated dashboard loading         | PASS    |
| Unauthorized access rejection           | PASS    |
| Invalid credentials rejection           | PASS    |
| CSV upload                              | PASS    |
| Invalid CSV rejection                   | PASS    |
| File size validation                    | PASS    |
| All seven supported cloud queries       | PASS    |
| Unsupported query rejection             | PASS    |
| EDA generation                          | PASS    |
| Groq executive summary generation       | PASS    |
| PowerPoint export                       | PASS    |
| Seven-slide report content verification | PASS    |
| Swagger documentation                   | PASS    |
| OpenAPI schema validation               | PASS    |
| Health check                            | PASS    |
| Cross-origin request protection         | PASS    |
| Public cloud deployment                 | PENDING |
| Hosted HTTPS verification               | PENDING |
| Hosted feature verification             | PENDING |

#### Automated API Testing

Testing tools:

- Pytest 9.2.0
- HTTPX 0.28.1
- FastAPI TestClient

Install testing dependencies:

```powershell
python -m pip install pytest httpx
```

Run automated tests:

```powershell
python -m pytest test_api.py -v
```

Save testing evidence:

```powershell
python -m pytest test_api.py -v | Tee-Object -FilePath test_results.txt
```

#### Automated Test Results

| Metric         | Result       |
| -------------- | ------------ |
| Total Tests    | 23           |
| Passed         | 23           |
| Failed         | 0            |
| Test Pass Rate | 100%         |
| Execution Time | 1.76 seconds |
| Warnings       | 1            |
| Overall Status | PASS         |

#### Individual Test Results

| No. | Test Case                       | Result |
| --: | ------------------------------- | ------ |
|   1 | Health check                    | PASS   |
|   2 | Unauthorized access             | PASS   |
|   3 | Invalid credentials             | PASS   |
|   4 | Authenticated dashboard access  | PASS   |
|   5 | Swagger documentation           | PASS   |
|   6 | OpenAPI schema                  | PASS   |
|   7 | Valid CSV upload                | PASS   |
|   8 | Missing required columns        | PASS   |
|   9 | Invalid numeric values          | PASS   |
|  10 | Negative deal values            | PASS   |
|  11 | Empty CSV rejection             | PASS   |
|  12 | File size validation            | PASS   |
|  13 | Supported questions endpoint    | PASS   |
|  14 | Customer count query            | PASS   |
|  15 | Total deal value query          | PASS   |
|  16 | Average deal value query        | PASS   |
|  17 | Minimum deal value query        | PASS   |
|  18 | Maximum deal value query        | PASS   |
|  19 | Deal stage distribution query   | PASS   |
|  20 | Sales performance query         | PASS   |
|  21 | Unsupported query rejection     | PASS   |
|  22 | EDA endpoint                    | PASS   |
|  23 | Cross-origin request protection | PASS   |

#### Testing Evidence

- Automated test script: `test_api.py`
- Test execution report: `test_results.txt`

The automated tests use synthetic CSV data and dummy
authentication credentials.

All 23 automated test cases passed successfully.

One Starlette TestClient dependency deprecation warning
was observed. It did not cause any test failures.

The 100% result represents the test pass rate,
not source code coverage.

Groq summary generation and PowerPoint export were
verified through separate manual testing.

The automated tests were executed locally in cloud mode.
Actual hosted application testing remains pending.

### 13. Verified Dataset Results

| Metric                           |          Value |
| -------------------------------- | -------------: |
| Total Records                    |            100 |
| Total Columns                    |             10 |
| Missing Values                   |              0 |
| Duplicate Records                |              0 |
| Total Deal Value                 | INR 24,875,000 |
| Average Deal Value               |    INR 248,750 |
| Median Deal Value                |    INR 237,500 |
| Minimum Deal Value               |     INR 15,000 |
| Maximum Deal Value               |    INR 500,000 |
| Top Three Representatives' Share |         59.84% |

### 14. PowerPoint Report

The generated PowerPoint report contains seven slides:

1. CRM Analytics Executive Report
2. Executive Summary
3. Key CRM Metrics
4. Sales Pipeline Distribution
5. Sales Representative Performance
6. Top Sales Insights
7. Business Recommendations

The complete AI-generated executive summary is included
in the speaker notes of Slide 2.

Output filename:

```text
CIA_CRM_Executive_Report.pptx
```

### 15. Security Measures

- Environment variables for API keys and credentials
- Git ignore rules for sensitive configuration files
- Password-protected cloud application
- Constant-time credential comparison
- Cross-origin POST request checks
- Restricted cloud analytics queries
- CSV size and structure validation
- Dataset version tracking
- Generic API error messages
- Cache prevention headers
- Clickjacking protection headers
- No execution of AI-generated Python in cloud mode
- Synthetic data and dummy credentials for automated testing

### 16. AI Tutor Architecture Review

Two AI Tutor interactions were completed to evaluate
the application architecture, security, performance,
deployment configuration, and testing requirements.

#### Interaction 1: Architecture Review

The following improvements were recommended:

- Stronger authentication mechanisms
- Secure environment-based secret management
- CSV input validation
- Automated API testing
- API documentation
- Health monitoring
- Rate limiting
- Persistent storage
- Background processing

#### Interaction 2: Deployment Validation

The AI Tutor considered the current architecture suitable
for a single-user internship demonstration.

Essential recommendations included:

- Authentication testing
- CSV validation testing
- Analytics query verification
- Health check validation
- Swagger documentation verification
- End-to-end application testing
- Secure handling of deployment credentials

#### Actions Taken

- Implemented 23 automated API tests.
- Verified all seven supported cloud queries.
- Verified authentication and unauthorized access rejection.
- Verified invalid CSV and oversized file rejection.
- Verified health check and Swagger documentation.
- Verified cross-origin request protection.
- Saved automated testing evidence.
- Updated project documentation.

Advanced authentication, persistent storage, rate limiting,
background workers, Docker, and CI/CD are potential
future enhancements.

The review was based on the described application
architecture. A complete source code review was not
performed by the AI Tutor.

### 17. Known Limitations

- Cloud mode supports only seven predefined analytics queries.
- Local natural language queries require a running Ollama server.
- PandasAI executes generated code and should only be used
  in a trusted local environment.
- Groq executive summary generation requires an internet
  connection and a valid API key.
- Groq API usage is subject to provider rate limits.
- AI-generated summaries may exceed the requested word count.
- AI summaries may contain unsupported interpretations
  and require human review.
- Recorded deal values do not necessarily represent
  realized revenue.
- Current deal stage counts do not establish conversion rates.
- Uploaded datasets and summaries are stored in memory.
- Data is lost when the server restarts.
- The application does not provide multi-user data isolation.
- The cloud application is intended for a single-user demo.
- HTTP Basic Authentication requires HTTPS for secure deployment.
- Password hash-based authentication is not implemented.
- Dedicated application-level rate limiting is not implemented.
- Free hosting may have resource limits and cold-start delays.
- Cloud dependency compatibility and hosted performance
  remain unverified.
- Full PowerPoint visual layout verification is pending.
- Automated source code coverage has not been measured.
- One TestClient dependency deprecation warning remains.

### 18. Deployment URL

Deployment Platform: Render

Deployment Status: Pending repository access approval.

Live Application URL: Pending

Live Dashboard URL: Pending

Live Swagger Documentation URL: Pending

An approval request has been sent to the internship team
before granting Render access to the GitHub repository.

### 19. Demo Video

Required Duration: 3 minutes

Recording Status: Pending

Demo Video Link: Pending

Planned demonstration:

1. Application introduction
2. Dashboard and authentication
3. CSV upload
4. CRM analytics and visualizations
5. Supported analytics queries
6. Automated EDA
7. Groq executive summary
8. PowerPoint report export
9. Swagger API documentation
10. Automated testing results

### 20. Project Completion Status

| Task                            | Status                             |
| ------------------------------- | ---------------------------------- |
| Application development         | Completed                          |
| Local configuration             | Completed                          |
| Cloud configuration             | Completed                          |
| Local application testing       | Completed                          |
| Simulated cloud testing         | Completed                          |
| Automated API testing           | Completed                          |
| Testing evidence                | Completed                          |
| AI Tutor interactions           | Completed                          |
| README documentation            | Completed - Deployment URL Pending |
| Repository access approval      | Pending                            |
| Complete source code review     | Pending                            |
| Render deployment               | Pending                            |
| Hosted application verification | Pending                            |
| Demo video recording            | Pending                            |
| Final GitHub pull request       | Pending                            |

### 21. Conclusion

The CIA CRM Analytics application has been successfully
configured and tested in local mode and simulated cloud mode.

CSV upload, analytics queries, EDA, executive summary
generation, and PowerPoint export have been verified.

All 23 automated API test cases passed successfully,
achieving a 100% test pass rate.

Two AI Tutor architecture review interactions were
completed, and relevant testing recommendations
were implemented.

Actual cloud deployment, hosted application validation,
demo video recording, and final pull request submission
remain pending.

### 22. Author

Praveen Kumar M

Data Analyst Intern

Cynaris Solutions Pvt. Ltd.

Week 8 - Day 4

Production Deployment and API Documentation
