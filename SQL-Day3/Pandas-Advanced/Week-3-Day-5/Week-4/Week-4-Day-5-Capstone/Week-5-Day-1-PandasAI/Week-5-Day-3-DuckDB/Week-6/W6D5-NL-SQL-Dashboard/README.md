# W6D5 – Natural Language SQL Dashboard on CRM Data

## 1. Project Overview

This project implements a Natural Language SQL Assistant for CRM data using Vanna AI, Ollama, SQLite, and FastAPI.

Users can ask questions in natural language and receive answers based on SQL queries executed against the CRM database.

## 2. Technologies Used

- Python 3.11.9
- Vanna AI 2.0.2
- Ollama
- Qwen 2.5:3B
- SQLite
- FastAPI
- Uvicorn
- Pandas

## 3. Project Structure

```text
W6D5-NL-SQL-Dashboard/
│
├── crm_data.csv
├── crm_database.db
├── create_database.ipynb
├── vanna_training.ipynb
├── main.py
├── README.md
│
└── evidence/
    ├── 01_api_customer_count.png
    └── 02_api_total_deal_value.png
```

## 4. Database Details

Database: `crm_database.db`

Table: `customers`

Total Records: 100

Columns:

- customer_id
- customer_name
- company
- lead_source
- sales_rep
- deal_value
- deal_stage
- status
- created_date
- last_activity

## 5. Vanna Agent Configuration

- Connected Vanna Agent to SQLite database.
- Configured Ollama using Qwen 2.5:3B.
- Created a custom CRM SQL execution tool named `run_sql`.
- Registered the SQL tool with the Tool Registry.
- Configured Agent Memory and Conversation Store.
- Created a CRM-specific system prompt.
- Trained the agent using five example question-SQL pairs.
- Verified retrieval of the saved training examples.

## 6. Natural Language Query Testing

Tested 10 natural-language questions against the CRM database.

The tests covered:

1. Total customer count.
2. Total deal value.
3. Customer count by deal stage.
4. Customer count by lead source.
5. Top five sales representatives by deal value.
6. Customer count by sales representative.
7. Won deals and their total deal value.
8. Customer count by status.
9. Average deal value by deal stage.
10. Monthly customer creation count.

SQL results were manually checked against the SQLite database.

Note: Some generated responses required correction or clarification, including an unnecessary status filter and currency formatting. These were identified during manual verification.

## 7. FastAPI Endpoint

Method: `POST`

Endpoint:

`/cia/sql-analyst`

Local URL:

`http://127.0.0.1:8000/cia/sql-analyst`

### Sample Request

```json
{
  "question": "How many customers are there in the CRM database?"
}
```

### Sample Response

```json
{
  "success": true,
  "conversation_id": "generated-conversation-id",
  "request_id": "generated-request-id",
  "answer": [
    {
      "type": "text",
      "text": "There are 100 customers in the CRM database."
    }
  ]
}
```

## 8. How to Run the Project

### Step 1: Activate Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2: Start Ollama

Ensure the Ollama application is running and the Qwen model is available.

```powershell
ollama run qwen2.5:3b
```

### Step 3: Navigate to Project Folder

Open the project folder in the terminal.

### Step 4: Start FastAPI Server

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Step 5: Open Swagger Documentation

`http://127.0.0.1:8000/docs`

Use the `POST /cia/sql-analyst` endpoint to submit CRM questions.

## 9. API Testing Results

| Test Question                 | Expected Result | HTTP Status |
| ----------------------------- | --------------- | ----------- |
| How many customers are there? | 100 customers   | 200         |
| What is the total deal value? | ₹2,48,75,000    | 200         |

Both API requests were successfully tested using Swagger UI.

## 10. Conclusion

The project demonstrates how natural-language questions can be converted into SQL operations using a Vanna AI Agent connected to an SQLite CRM database.

FastAPI exposes the agent through a custom REST API endpoint, allowing users to interact with CRM data using natural language.
