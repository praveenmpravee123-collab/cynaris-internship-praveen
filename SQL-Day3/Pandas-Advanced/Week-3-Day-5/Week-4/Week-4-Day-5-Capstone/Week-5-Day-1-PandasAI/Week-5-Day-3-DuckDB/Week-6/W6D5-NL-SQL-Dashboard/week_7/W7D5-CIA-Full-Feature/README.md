# CIA Full Feature – CRM Data Analytics Dashboard

## Week 7 Day 5 | Cynaris Data Analyst Internship

### 1. Project Overview

CIA (Customer Intelligence Analytics) is an interactive CRM analytics dashboard that combines CSV upload, automated data analysis, visualizations, and natural-language querying.

The application uses FastAPI, Pandas, PandasAI, a locally hosted Ollama LLM, and Chart.js to help users explore CRM data.

### 2. Project Objectives

- Upload and analyze CRM datasets through a web interface.
- Process CSV data using Pandas.
- Display customer and sales performance metrics.
- Generate interactive charts using Chart.js.
- Answer natural-language questions using PandasAI and Ollama.
- Validate uploaded data and handle invalid queries.

### 3. Technologies Used

| Technology            | Purpose                          |
| --------------------- | -------------------------------- |
| Python                | Backend programming              |
| FastAPI               | REST API development             |
| Pandas                | CSV processing and data analysis |
| PandasAI              | Natural-language data queries    |
| Ollama                | Free local LLM execution         |
| Qwen 2.5 3B           | Language model                   |
| Chart.js              | Interactive dashboard charts     |
| HTML, CSS, JavaScript | Frontend dashboard               |
| Jupyter Notebook      | Data exploration and testing     |

### 4. Dataset Information

The CRM dataset contains:

- **100 customer records**
- **10 columns**
- **Total Deal Value:** ₹2,48,75,000
- **Average Deal Value:** ₹2,48,750

Key columns include `customer_id`, `customer_name`, `company`, `lead_source`, `sales_rep`, `deal_value`, `deal_stage`, `status`, `created_date`, and `last_activity`.

### 5. Features Implemented

**CSV Upload**

Users can upload a CRM CSV file through the dashboard. FastAPI validates the file and Pandas processes its contents.

**CRM Analytics**

The dashboard displays total customers, total deal value, deal stage distribution, and sales representative performance.

**Natural-Language Queries**

Users can ask questions about the uploaded dataset. PandasAI processes questions using the locally hosted Ollama Qwen model.

**Error Handling**

The backend checks file type, file size, required columns, invalid values, empty questions, and certain explicitly referenced nonexistent columns.

**Interactive Visualizations**

Chart.js renders a doughnut chart for deal stages and a bar chart for sales representative performance.

### 6. Project Files

```text
W7D5-CIA-Full-Feature/
├── W7D5_CIA_Full_Feature.ipynb
├── csv_upload_api.py
├── dashboard.html
├── chart_data.json
├── README.md
└── evidence/
    ├── 01_cia_chartjs_dashboard.png
    ├── 02_csv_upload_api_success.png
    ├── 03_dynamic_csv_dashboard.png
    ├── 04_pandasai_query_api_success.png
    └── 05_ai_natural_language_query_success.png
```

The CRM dataset is loaded from the parent project directory.

### 7. How to Run

**Step 1 – Start Ollama**

Ensure Ollama is running locally and the `qwen2.5:3b` model is available.

**Step 2 – Start FastAPI**

From the `W7D5-CIA-Full-Feature` folder, run:

```powershell
python -m uvicorn csv_upload_api:app --host 127.0.0.1 --port 8002
```

**Step 3 – Start Frontend Server**

From the same folder, open another terminal and run:

```powershell
python -m http.server 8001
```

**Step 4 – Open Dashboard**

Navigate to:

`http://localhost:8001/dashboard.html`

**Step 5 – Upload Dataset**

Select `crm_data.csv` and click **Upload CSV**.

**Step 6 – Ask Questions**

Enter natural-language questions in the AI query section and click **Ask AI**.

### 8. API Endpoints

| Endpoint          | Method | Description                        |
| ----------------- | ------ | ---------------------------------- |
| `/`               | GET    | API health check                   |
| `/cia/upload-csv` | POST   | Upload and analyze CSV             |
| `/cia/query`      | POST   | Query uploaded data using PandasAI |
| `/docs`           | GET    | FastAPI Swagger documentation      |

### 9. Testing Results

| Test Case                           | Expected Result          | Status |
| ----------------------------------- | ------------------------ | ------ |
| Customer count                      | 100                      | Passed |
| Total deal value                    | ₹2,48,75,000             | Passed |
| Won stage count                     | 22                       | Passed |
| Average deal value                  | ₹2,48,750                | Passed |
| Highest sales representative        | Rahul Menon – ₹52,15,000 | Passed |
| Invalid column reference            | Clear validation error   | Passed |
| Valid query after validation update | ₹2,48,75,000             | Passed |

### 10. Known Limitations

- PandasAI answers can vary depending on question wording.
- Column validation covers selected explicit naming patterns, not every possible invalid reference.
- Uploaded data is stored in server memory and is cleared when the backend restarts.
- The current implementation stores one active dataset for the application, rather than separate datasets per user session.
- Chart data is formatted for Chart.js rather than Plotly JSON.
- The application is intended for local development and demonstration, not public production deployment.

### 11. Conclusion

The CIA Full Feature project integrates CRM data processing, interactive visualizations, and natural-language analytics into a single dashboard.

The tested functionality demonstrates CSV upload, FastAPI integration, PandasAI querying with a free local LLM, and basic input validation.

**Project:** Cynaris Data Analyst Internship – Week 7 Day 5
