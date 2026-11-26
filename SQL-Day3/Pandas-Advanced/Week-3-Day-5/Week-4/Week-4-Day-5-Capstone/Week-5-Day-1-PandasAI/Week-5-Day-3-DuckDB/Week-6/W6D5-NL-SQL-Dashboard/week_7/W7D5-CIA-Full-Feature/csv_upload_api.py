from io import BytesIO
from pathlib import Path
from typing import Optional
from collections import Counter
import asyncio
import logging
import math
import os
import re
import threading
import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
# ==================================================
# 1. FASTAPI CONFIGURATION
# ==================================================
app = FastAPI(
    title="CIA Full Feature API",
    description="CSV Upload, EDA, PandasAI, Groq Summary and PPT Export",
    version="1.6.0"
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cia_api")
# ==================================================
# 2. PANDASAI + OLLAMA
# ==================================================
llm = LiteLLM(
    model="ollama/qwen2.5:3b",
    api_base="http://localhost:11434"
)
pai.config.set({"llm": llm})
print("PandasAI + Ollama configured successfully!")
# ==================================================
# 3. GROQ ENVIRONMENT
# ==================================================
BASE_DIR = Path(__file__).resolve().parent
def find_groq_env():
    for folder in [BASE_DIR, *BASE_DIR.parents]:
        possible_files = [
            folder / ".env",
            folder / "week_8" / "W8D1-Executive-Summary" / ".env"
        ]
        for env_file in possible_files:
            if env_file.is_file():
                load_dotenv(env_file, override=False)
        if os.getenv("GROQ_API_KEY"):
            return True
    return False
groq_configured = find_groq_env()
if groq_configured:
    print("Groq API key loaded successfully!")
else:
    print("Groq API key not found!")
# ==================================================
# 4. GLOBAL DATASET
# ==================================================
current_df: Optional[pd.DataFrame] = None
current_summary = None
data_lock = threading.Lock()
query_lock = threading.Lock()
REQUIRED_COLUMNS = {
    "deal_stage",
    "sales_rep",
    "deal_value"
}
MAX_FILE_SIZE = 5 * 1024 * 1024
def get_uploaded_dataframe():
    with data_lock:
        if current_df is None:
            raise HTTPException(
                status_code=400,
                detail="Please upload a CSV file first."
            )
        return current_df.copy()
# ==================================================
# 5. JSON CONVERSION
# ==================================================
def json_safe(value):
    if isinstance(value, dict):
        return {
            str(k): json_safe(v)
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, pd.DataFrame):
        return json_safe(value.to_dict(orient="records"))
    if isinstance(value, pd.Series):
        return json_safe(value.to_dict())
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_safe(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value
# ==================================================
# 6. HEALTH CHECK
# ==================================================
@app.get("/")
def home():
    return {
        "success": True,
        "message": "CIA Full Feature API is running",
        "groq_configured": groq_configured
    }
# ==================================================
# 7. CHART DATA
# ==================================================
def generate_chart_data(df):
    stages = df["deal_stage"].value_counts()
    sales = (
        df.groupby("sales_rep")["deal_value"]
        .sum()
        .sort_values(ascending=False)
    )
    return {
        "deal_stage": {
            "labels": stages.index.tolist(),
            "datasets": [{
                "label": "Customer Count",
                "data": [int(v) for v in stages.values]
            }]
        },
        "sales_performance": {
            "labels": sales.index.tolist(),
            "datasets": [{
                "label": "Total Deal Value (INR)",
                "data": [float(v) for v in sales.values]
            }]
        }
    }
# ==================================================
# 8. CSV UPLOAD
# ==================================================
@app.post("/cia/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    global current_df, current_summary
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
                detail="CSV exceeds the 5 MB limit."
            )
        try:
            df = pd.read_csv(BytesIO(content))
        except (pd.errors.ParserError, UnicodeDecodeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Unable to read CSV file."
            )
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="CSV file is empty."
            )
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise HTTPException(
                status_code=400,
                detail="Missing required columns: " + ", ".join(sorted(missing))
            )
        df["deal_value"] = pd.to_numeric(
            df["deal_value"],
            errors="coerce"
        )
        if df["deal_value"].isna().any():
            raise HTTPException(
                status_code=400,
                detail="Invalid deal_value values."
            )
        if df["deal_stage"].isna().any() or df["sales_rep"].isna().any():
            raise HTTPException(
                status_code=400,
                detail="deal_stage and sales_rep cannot contain missing values."
            )
        charts = generate_chart_data(df)
        with data_lock:
            current_df = df.copy()
            current_summary = None
        return {
            "success": True,
            "filename": file.filename,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "total_deal_value": float(df["deal_value"].sum()),
            "charts": charts
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("CSV upload failed")
        raise HTTPException(
            status_code=500,
            detail="CSV processing failed."
        )
    finally:
        await file.close()
# ==================================================
# 9. EDA GENERATION
# ==================================================
def generate_eda(df):
    numeric_statistics = {}
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()
    for column in numeric_columns:
        series = df[column].dropna()
        if series.empty:
            numeric_statistics[column] = {
                "count": 0,
                "mean": None,
                "median": None,
                "minimum": None,
                "maximum": None,
                "standard_deviation": None
            }
        else:
            numeric_statistics[column] = {
                "count": int(series.count()),
                "mean": json_safe(series.mean()),
                "median": json_safe(series.median()),
                "minimum": json_safe(series.min()),
                "maximum": json_safe(series.max()),
                "standard_deviation": json_safe(series.std())
            }
    stages = {
        str(k): int(v)
        for k, v in df["deal_stage"].value_counts().items()
    }
    sales = {
        str(k): float(v)
        for k, v in (
            df.groupby("sales_rep")["deal_value"]
            .sum()
            .sort_values(ascending=False)
            .items()
        )
    }
    return {
        "success": True,
        "dataset_overview": {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "column_names": df.columns.tolist(),
            "duplicates": int(df.duplicated().sum()),
            "missing_values": {
                str(k): int(v)
                for k, v in df.isna().sum().items()
            },
            "total_missing_values": int(df.isna().sum().sum())
        },
        "numeric_statistics": numeric_statistics,
        "crm_insights": {
            "total_customers": int(len(df)),
            "total_deal_value": float(df["deal_value"].sum()),
            "average_deal_value": float(df["deal_value"].mean()),
            "deal_stage_distribution": stages,
            "sales_performance": sales
        }
    }
@app.get("/cia/eda")
def cia_eda():
    df = get_uploaded_dataframe()
    try:
        return json_safe(generate_eda(df))
    except Exception:
        logger.exception("EDA generation failed")
        raise HTTPException(
            status_code=500,
            detail="EDA generation failed."
        )
# ==================================================
# 10. PANDASAI QUERY
# ==================================================
class CIAQueryRequest(BaseModel):
    question: str
def validate_column_references(question, df):
    patterns = [
        r"\bcolumn\s+(?:named|called)\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        r"\bthe\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)[`'\"]?\s+column\b"
    ]
    referenced = set()
    for pattern in patterns:
        referenced.update(
            re.findall(pattern, question, flags=re.IGNORECASE)
        )
    existing = {str(c).lower() for c in df.columns}
    missing = [
        c for c in referenced
        if c.lower() not in existing
    ]
    if missing:
        raise HTTPException(
            status_code=400,
            detail="Column not found: " + ", ".join(sorted(missing))
        )
def process_pandasai_query(question, df):
    improved_question = f"""
{question}
IMPORTANT CODE GENERATION INSTRUCTIONS:
1. Use execute_sql_query() for SQL operations.
2. execute_sql_query() returns a pandas DataFrame.
3. For a single numeric answer, extract the first cell
   using .iloc[0, 0].
4. Convert numeric values to float or int.
5. Always declare a dictionary named result.
6. result must contain exactly "type" and "value".
For numeric answers, use this pattern:
sql_result = execute_sql_query("SELECT ...")
numeric_value = float(sql_result.iloc[0, 0])
result = {{"type": "number", "value": numeric_value}}
Never put a DataFrame directly inside a number result.
For text:
result = {{"type": "string", "value": "answer text"}}
For tables:
result = {{"type": "dataframe", "value": sql_result}}
Return executable Python code.
"""
    with query_lock:
        smart_df = pai.DataFrame(df)
        response = smart_df.chat(improved_question)
    if getattr(response, "type", None) == "error":
        raise ValueError(
            "PandasAI could not answer: " + str(response.value)
        )
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
@app.post("/cia/query")
async def cia_query(request: CIAQueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )
    df = get_uploaded_dataframe()
    validate_column_references(question, df)
    try:
        answer = await asyncio.to_thread(
            process_pandasai_query,
            question,
            df
        )
        return {
            "success": True,
            "question": question,
            "answer": json_safe(answer)
        }
    except Exception as error:
        logger.exception("PandasAI query failed")
        raise HTTPException(
            status_code=500,
            detail=f"PandasAI query failed: {error}"
        )
# ==================================================
# 11. GROQ EXECUTIVE SUMMARY
# ==================================================
def generate_executive_summary(eda_data):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found.")
    insights = eda_data["crm_insights"]
    overview = eda_data["dataset_overview"]
    stages = insights["deal_stage_distribution"]
    sales = insights["sales_performance"]
    total_value = insights["total_deal_value"]
    average_value = insights["average_deal_value"]
    top_three_total = sum(sorted(sales.values(), reverse=True)[:3])
    top_three_share = 100 * top_three_total / total_value if total_value else 0
    prompt = f"""
You are a professional CRM business analyst.
Write a concise executive summary of 180 to 220 words. Do not include headings with numbering or arithmetic expressions.
Use ONLY these verified facts:
Total records: {overview["rows"]}
Total columns: {overview["columns"]}
Missing values: {overview["total_missing_values"]}
Duplicate records: {overview["duplicates"]}
Total deal value (INR): {total_value}
Average deal value (INR): {average_value}
Current deal stages:
{stages}
Deal value by sales representative:
{sales}
REQUIRED STRUCTURE:
1. Dataset and data quality
2. Deal value and pipeline observations
3. Sales representative performance
4. Actionable recommendations
CRITICAL ACCURACY RULES:
- Total deal value is not necessarily realized revenue.
- Current stage counts are NOT conversion rates.
- Never calculate Won / Qualified as a conversion rate.
- Do not invent historical trends or causal explanations.
- Do not mention top-three share or remaining share; the application appends the verified percentage separately.
- Clearly distinguish observations from recommendations.
- Use INR for monetary values.
- Return only the executive summary.
"""
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Write concise, accurate business reports. "
                    "Do not invent statistics."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=2000,
        reasoning_effort="low"
    )
    if not response.choices:
        raise ValueError("Groq returned no response choices.")
    choice = response.choices[0]
    summary = choice.message.content
    if not summary or not summary.strip():
        raise ValueError(
            "Groq returned empty content. "
            f"Finish reason: {choice.finish_reason}"
        )
    # Reject unsupported percentage claims instead of silently exporting them.
    if "%" in summary or re.search(r"\bpercent(?:age)?\b", summary, re.IGNORECASE):
        raise ValueError("AI summary contains an unverified percentage; retry generation.")
    return (summary.strip() + f"\n\nVerified top-three share of recorded deal value: {top_three_share:.2f}%.")
@app.post("/cia/executive-summary")
async def cia_executive_summary():
    global current_summary
    df = get_uploaded_dataframe()
    if not groq_configured:
        raise HTTPException(
            status_code=503,
            detail="Groq API key not configured."
        )
    try:
        eda = generate_eda(df)
        summary = await asyncio.to_thread(
            generate_executive_summary,
            eda
        )
        with data_lock:
            if current_df is not None and current_df.equals(df):
                current_summary = summary
        insights = eda["crm_insights"]
        return {
            "success": True,
            "model": "openai/gpt-oss-20b",
            "dataset_rows": int(len(df)),
            "executive_summary": summary,
            "word_count": len(summary.split()),
            "insights": {
                "total_customers": insights["total_customers"],
                "total_deal_value": insights["total_deal_value"],
                "average_deal_value": insights["average_deal_value"],
                "deal_stage_distribution": insights[
                    "deal_stage_distribution"
                ]
            }
        }
    except Exception:
        logger.exception("Groq summary generation failed")
        raise HTTPException(
            status_code=500,
            detail="Executive summary generation failed. Check server logs."
        )
# ==================================================
# 12. POWERPOINT HELPERS
# ==================================================
NAVY = RGBColor(22, 37, 66)
BLUE = RGBColor(44, 104, 190)
GRAY = RGBColor(85, 95, 110)
def add_text_slide(prs, title, lines):
    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )
    title_box = slide.shapes.add_textbox(
        Inches(0.6),
        Inches(0.4),
        Inches(11.9),
        Inches(0.8)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    for paragraph in title_frame.paragraphs:
        paragraph.font.size = Pt(27)
        paragraph.font.bold = True
        paragraph.font.color.rgb = NAVY
    body_box = slide.shapes.add_textbox(
        Inches(0.8),
        Inches(1.5),
        Inches(11.6),
        Inches(5.3)
    )
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    for index, line in enumerate(lines):
        if index == 0:
            paragraph = body_frame.paragraphs[0]
        else:
            paragraph = body_frame.add_paragraph()
        paragraph.text = line
        paragraph.font.size = Pt(19)
        paragraph.font.color.rgb = GRAY
        paragraph.space_after = Pt(16)
    return slide
def add_chart_slide(prs, title, labels, values, chart_type):
    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )
    title_box = slide.shapes.add_textbox(
        Inches(0.6),
        Inches(0.3),
        Inches(12),
        Inches(0.7)
    )
    title_box.text_frame.text = title
    for paragraph in title_box.text_frame.paragraphs:
        paragraph.font.size = Pt(27)
        paragraph.font.bold = True
        paragraph.font.color.rgb = NAVY
    chart_data = CategoryChartData()
    chart_data.categories = labels
    chart_data.add_series(
        "Value",
        values
    )
    chart_shape = slide.shapes.add_chart(
        chart_type,
        Inches(0.7),
        Inches(1.3),
        Inches(11.8),
        Inches(5.5),
        chart_data
    )
    chart = chart_shape.chart
    chart.has_legend = False
    return slide
# ==================================================
# 13. VERIFIED POWERPOINT GENERATION
# ==================================================
def generate_powerpoint(df, executive_summary):
    eda = generate_eda(df)
    overview = eda["dataset_overview"]
    insights = eda["crm_insights"]
    total = insights["total_deal_value"]
    average = insights["average_deal_value"]
    stages = insights["deal_stage_distribution"]
    sales = insights["sales_performance"]
    ranked_sales = sorted(
        sales.items(),
        key=lambda item: item[1],
        reverse=True
    )
    top_three = ranked_sales[:3]
    top_three_total = sum(
        value for _, value in top_three
    )
    top_three_share = (
        100 * top_three_total / total
        if total != 0 else 0
    )
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    # Slide 1: Title
    add_text_slide(
        prs,
        "CRM Analytics - Executive Report",
        [
            "Conversational Insights Automation (CIA)",
            f"Dataset: {overview['rows']} CRM records",
            "EDA, Sales Pipeline and Business Recommendations",
            "Prepared using validated CRM analytics"
        ]
    )
    # Slide 2: Executive Summary
    add_text_slide(
        prs,
        "Executive Summary",
        [
            (
                f"The CRM dataset contains {overview['rows']} records "
                f"across {overview['columns']} fields."
            ),
            (
                f"Total recorded deal value is INR {total:,.0f}; "
                f"average deal value is INR {average:,.0f}."
            ),
            (
                f"The current pipeline includes "
                f"{stages.get('Qualified', 0)} Qualified, "
                f"{stages.get('Won', 0)} Won and "
                f"{stages.get('Lost', 0)} Lost records."
            ),
            (
                f"The top three representatives account for "
                f"{top_three_share:.1f}% of total recorded deal value."
            ),
            (
                "Deal values are pipeline amounts, not necessarily "
                "realized revenue. Stage counts do not establish "
                "historical conversion rates."
            )
        ]
    )
    # Preserve the full AI summary in slide 2 speaker notes.
    prs.slides[1].notes_slide.notes_text_frame.text = executive_summary
    # Slide 3: Key Metrics
    add_text_slide(
        prs,
        "Key CRM Metrics",
        [
            f"Total Records: {overview['rows']}",
            f"Total Deal Value: INR {total:,.0f}",
            f"Average Deal Value: INR {average:,.0f}",
            f"Missing Values: {overview['total_missing_values']}",
            f"Duplicate Records: {overview['duplicates']}"
        ]
    )
    # Slide 4: Pipeline Chart
    add_chart_slide(
        prs,
        "Sales Pipeline Distribution",
        list(stages.keys()),
        list(stages.values()),
        XL_CHART_TYPE.COLUMN_CLUSTERED
    )
    # Slide 5: Sales Performance Chart
    add_chart_slide(
        prs,
        "Sales Representative Performance",
        list(sales.keys()),
        list(sales.values()),
        XL_CHART_TYPE.BAR_CLUSTERED
    )
    # Slide 6: Sales Insights
    top_lines = [
        (
            f"{index}. {name}: INR {value:,.0f}"
        )
        for index, (name, value) in enumerate(
            top_three,
            start=1
        )
    ]
    top_lines.append(
        f"Top-three share of total deal value: {top_three_share:.1f}%"
    )
    top_lines.append(
        "These figures represent recorded deal values, "
        "not confirmed revenue."
    )
    add_text_slide(
        prs,
        "Top Sales Insights",
        top_lines
    )
    # Slide 7: Recommendations
    add_text_slide(
        prs,
        "Business Recommendations",
        [
            "Review Lost deals to identify recurring reasons and possible improvements.",
            "Prioritize follow-up for Proposal and Negotiation records.",
            "Share effective practices from high-performing sales representatives.",
            "Continue monitoring missing values and duplicate records.",
            "Track stage transitions over time before calculating conversion rates."
        ]
    )
    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output
# ==================================================
# 14. PPT EXPORT ENDPOINT
# ==================================================
@app.post("/cia/export-ppt")
async def cia_export_ppt():
    with data_lock:
        if current_df is None:
            raise HTTPException(status_code=400, detail="Please upload a CSV file first.")
        df = current_df.copy()
        summary = current_summary
    if not summary:
        raise HTTPException(status_code=400, detail="Generate the executive summary before exporting PPT.")
    try:
        ppt_stream = await asyncio.to_thread(
            generate_powerpoint,
            df,
            summary
        )
        return StreamingResponse(
            ppt_stream,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
            headers={
                "Content-Disposition": (
                    'attachment; filename="CIA_CRM_Executive_Report.pptx"'
                )
            }
        )
    except Exception:
        logger.exception("PPT export failed")
        raise HTTPException(
            status_code=500,
            detail="PPT export failed. Check server logs."
        )
# ==================================================
# 15. STARTUP INFORMATION
# ==================================================
print("CIA Full Feature API initialized!")
print("CSV Upload: POST /cia/upload-csv")
print("EDA: GET /cia/eda")
print("PandasAI Query: POST /cia/query")
print("Groq Summary: POST /cia/executive-summary")
print("PPT Export: POST /cia/export-ppt")
print("LLM: Ollama qwen2.5:3b")
print("Summary Model: Groq openai/gpt-oss-20b")
