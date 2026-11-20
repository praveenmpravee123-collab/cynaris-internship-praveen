
from io import BytesIO
from typing import Optional
import asyncio
import re
import threading

import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# --------------------------------------------------
# 1. Initialize FastAPI
# --------------------------------------------------

app = FastAPI(
    title="CIA Full Feature API",
    description="CSV Upload, CRM Analytics and PandasAI Queries",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


# --------------------------------------------------
# 2. Configure PandasAI with Local Ollama
# --------------------------------------------------

llm = LiteLLM(
    model="ollama/qwen2.5:3b",
    api_base="http://localhost:11434"
)

pai.config.set({"llm": llm})

print("PandasAI + Ollama configured successfully!")


# --------------------------------------------------
# 3. Dataset Storage and Settings
# --------------------------------------------------

current_df: Optional[pd.DataFrame] = None

data_lock = threading.Lock()
query_lock = threading.Lock()

REQUIRED_COLUMNS = {
    "deal_stage",
    "sales_rep",
    "deal_value"
}

MAX_FILE_SIZE = 5 * 1024 * 1024


# --------------------------------------------------
# 4. Health Check
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "CIA Full Feature API is running",
        "status": "success"
    }


# --------------------------------------------------
# 5. Chart.js Data Generation
# --------------------------------------------------

def generate_chart_data(df: pd.DataFrame):

    stage_counts = df["deal_stage"].value_counts()

    sales_performance = (
        df.groupby("sales_rep")["deal_value"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "deal_stage": {
            "labels": stage_counts.index.tolist(),
            "datasets": [
                {
                    "label": "Customer Count",
                    "data": [
                        int(value)
                        for value in stage_counts.values
                    ]
                }
            ]
        },
        "sales_performance": {
            "labels": sales_performance.index.tolist(),
            "datasets": [
                {
                    "label": "Total Deal Value (INR)",
                    "data": [
                        float(value)
                        for value in sales_performance.values
                    ]
                }
            ]
        }
    }


# --------------------------------------------------
# 6. CSV Upload Endpoint
# --------------------------------------------------

@app.post("/cia/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    global current_df

    try:
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid CSV file."
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="CSV file exceeds the 5 MB size limit."
            )

        try:
            df = pd.read_csv(BytesIO(content))
        except (
            pd.errors.ParserError,
            UnicodeDecodeError,
            ValueError
        ):
            raise HTTPException(
                status_code=400,
                detail="Unable to read the CSV file."
            )

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV file is empty."
            )

        missing_columns = REQUIRED_COLUMNS - set(df.columns)

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Missing required columns: "
                    + ", ".join(sorted(missing_columns))
                )
            )

        df["deal_value"] = pd.to_numeric(
            df["deal_value"],
            errors="coerce"
        )

        if df["deal_value"].isna().any():
            raise HTTPException(
                status_code=400,
                detail="The deal_value column contains invalid values."
            )

        if df["deal_stage"].isna().any() or df["sales_rep"].isna().any():
            raise HTTPException(
                status_code=400,
                detail="deal_stage and sales_rep cannot contain missing values."
            )

        charts = generate_chart_data(df)

        with data_lock:
            current_df = df.copy()

        return {
            "success": True,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "total_deal_value": float(df["deal_value"].sum()),
            "charts": charts
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"CSV processing failed: {str(error)}"
        )

    finally:
        await file.close()


# --------------------------------------------------
# 7. Validate Explicit Column References
# --------------------------------------------------

def validate_column_references(question: str, df: pd.DataFrame):
    """
    Check explicitly named columns.

    Supported examples:
    - column named imaginary_sales_amount
    - column called imaginary_sales_amount
    - the imaginary_sales_amount column

    This is a limited safeguard, not a guarantee
    that every nonexistent column will be detected.
    """

    patterns = [
        r"\bcolumn\s+(?:named|called)\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        r"\bthe\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)[`'\"]?\s+column\b"
    ]

    referenced_columns = set()

    for pattern in patterns:
        matches = re.findall(
            pattern,
            question,
            flags=re.IGNORECASE
        )

        referenced_columns.update(matches)

    existing_columns = {
        str(column).lower()
        for column in df.columns
    }

    missing_columns = [
        column
        for column in referenced_columns
        if column.lower() not in existing_columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=(
                "Column not found in uploaded CSV: "
                + ", ".join(sorted(missing_columns))
            )
        )


# --------------------------------------------------
# 8. PandasAI Query Processing
# --------------------------------------------------

class CIAQueryRequest(BaseModel):
    question: str


def process_pandasai_query(question: str, df: pd.DataFrame):

    with query_lock:
        smart_df = pai.DataFrame(df)

        response = smart_df.chat(question)

        print(
            "PandasAI RAW RESPONSE:",
            repr(response),
            flush=True
        )

    # Detect PandasAI ErrorResponse
    if getattr(response, "type", None) == "error":
        raise ValueError(
            "PandasAI could not answer this question: "
            + str(response.value)
        )

    # Convert PandasAI response to JSON-compatible data
    if isinstance(response, pd.DataFrame):
        return response.to_dict(orient="records")

    if isinstance(response, pd.Series):
        return response.to_dict()

    if isinstance(response, (int, float, str, bool)):
        return response

    if hasattr(response, "value"):

        value = response.value

        if isinstance(value, pd.DataFrame):
            return value.to_dict(orient="records")

        if isinstance(value, pd.Series):
            return value.to_dict()

        if isinstance(value, (int, float, str, bool, list, dict)):
            return value

    return str(response)


# --------------------------------------------------
# 9. Natural Language Query Endpoint
# --------------------------------------------------

@app.post("/cia/query")
async def cia_query(request: CIAQueryRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    with data_lock:

        if current_df is None:
            raise HTTPException(
                status_code=400,
                detail="Please upload a CSV file first."
            )

        df_copy = current_df.copy()

    # Validate before calling the LLM
    validate_column_references(question, df_copy)

    try:
        answer = await asyncio.to_thread(
            process_pandasai_query,
            question,
            df_copy
        )

        return {
            "success": True,
            "question": question,
            "answer": answer
        }

    except Exception as error:
        print(
            "PandasAI Query Error:",
            str(error),
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail=f"PandasAI query failed: {str(error)}"
        )


# --------------------------------------------------
# 10. Startup Information
# --------------------------------------------------

print("CIA Full Feature API initialized!")
print("CSV Upload: POST /cia/upload-csv")
print("PandasAI Query: POST /cia/query")
print("LLM: Ollama qwen2.5:3b")
