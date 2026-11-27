import os

import pytest
from fastapi.testclient import TestClient

# Isolated cloud-mode test configuration
os.environ["APP_ENV"] = "cloud"
os.environ["DEMO_USERNAME"] = "test_user"
os.environ["DEMO_PASSWORD"] = "TestOnlyPassword2026"

from csv_upload_api import app

client = TestClient(app)

AUTH = ("test_user", "TestOnlyPassword2026")

CSV_DATA = (
    "deal_stage,sales_rep,deal_value\n"
    "Won,Rahul,10000\n"
    "Qualified,Priya,20000\n"
    "Lost,Rahul,30000\n"
)

HEADERS = {"Origin": "http://testserver"}


def upload_csv(content=CSV_DATA):
    return client.post(
        "/cia/upload-csv",
        files={
            "file": ("test_crm.csv", content, "text/csv")
        },
        auth=AUTH,
        headers=HEADERS,
    )


@pytest.fixture
def uploaded_dataset():
    response = upload_csv()
    assert response.status_code == 200, response.text


# 1. Health check
def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200


# 2. Unauthorized access
def test_unauthorized_access():
    response = client.get("/dashboard")
    assert response.status_code == 401


# 3. Invalid credentials
def test_invalid_credentials():
    response = client.get(
        "/dashboard",
        auth=("wrong_user", "wrong_password"),
    )
    assert response.status_code == 401


# 4. Valid credentials
def test_dashboard_access():
    response = client.get("/dashboard", auth=AUTH)
    assert response.status_code == 200


# 5. Swagger documentation
def test_swagger_documentation():
    response = client.get("/docs", auth=AUTH)
    assert response.status_code == 200


# 6. OpenAPI schema
def test_openapi_schema():
    response = client.get("/openapi.json", auth=AUTH)
    assert response.status_code == 200
    assert "/cia/query" in response.json()["paths"]


# 7. Valid CSV upload
def test_valid_csv_upload():
    response = upload_csv()
    assert response.status_code == 200, response.text


# 8. Missing required columns
def test_missing_columns():
    response = upload_csv("name,age\nRahul,25\n")
    assert response.status_code in (400, 422)


# 9. Invalid numeric values
def test_invalid_deal_value():
    response = upload_csv(
        "deal_stage,sales_rep,deal_value\n"
        "Won,Rahul,invalid\n"
    )
    assert response.status_code in (400, 422)


# 10. Negative deal values
def test_negative_deal_value():
    response = upload_csv(
        "deal_stage,sales_rep,deal_value\n"
        "Won,Rahul,-1000\n"
    )
    assert response.status_code in (400, 422)


# 11. Empty CSV
def test_empty_csv():
    response = upload_csv("")
    assert response.status_code in (400, 422)


# 12. File size validation
def test_large_csv():
    response = upload_csv(b"x" * (6 * 1024 * 1024))
    assert response.status_code in (400, 413, 422)


# 13. Supported questions
def test_supported_questions():
    response = client.get(
        "/cia/supported-questions",
        auth=AUTH,
    )
    assert response.status_code == 200


# 14-18. Numerical analytics queries
@pytest.mark.parametrize(
    "question,expected",
    [
        ("How many customers are there?", 3),
        ("What is the total deal value?", 60000),
        ("What is the average deal value?", 20000),
        ("What is the minimum deal value?", 10000),
        ("What is the maximum deal value?", 30000),
    ],
)
def test_numeric_queries(uploaded_dataset, question, expected):
    response = client.post(
        "/cia/query",
        json={"question": question},
        auth=AUTH,
        headers=HEADERS,
    )

    assert response.status_code == 200, response.text

    result = response.json()
    assert float(result["answer"]) == expected


# 19-20. Distribution queries
@pytest.mark.parametrize(
    "question",
    [
        "Show deal stage distribution",
        "Show sales performance",
    ],
)
def test_distribution_queries(uploaded_dataset, question):
    response = client.post(
        "/cia/query",
        json={"question": question},
        auth=AUTH,
        headers=HEADERS,
    )

    assert response.status_code == 200, response.text
    assert response.json().get("answer") is not None


# 21. Unsupported query rejection
def test_unsupported_query(uploaded_dataset):
    response = client.post(
        "/cia/query",
        json={"question": "Show all customer names"},
        auth=AUTH,
        headers=HEADERS,
    )

    assert response.status_code in (400, 422)


# 22. EDA endpoint
def test_eda(uploaded_dataset):
    response = client.get("/cia/eda", auth=AUTH)
    assert response.status_code == 200, response.text


# 23. Cross-origin request protection
def test_cross_origin_protection():
    response = client.post(
        "/cia/query",
        json={"question": "What is the total deal value?"},
        auth=AUTH,
        headers={"Origin": "https://untrusted.example"},
    )

    assert response.status_code == 403