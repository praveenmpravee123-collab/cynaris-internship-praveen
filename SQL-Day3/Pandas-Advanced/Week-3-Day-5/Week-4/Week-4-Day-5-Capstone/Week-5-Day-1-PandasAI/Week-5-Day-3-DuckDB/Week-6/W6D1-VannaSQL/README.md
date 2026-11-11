# Vanna AI SQL Analyst

## Project Overview

This project implements a Text-to-SQL application using Vanna AI, Ollama, SQLite, and FastAPI.

Users can ask questions in natural language, and the AI agent generates SQL queries to retrieve information from the job market database.

## Technologies Used

- Python
- Vanna AI
- Ollama
- Qwen 2.5 (3B)
- SQLite
- FastAPI
- Uvicorn

## Dataset

Dataset: job_market_india_100k.csv

Database: job_market.db

Table: job_market

Columns:

- Job Title
- Location
- Salary
- Monthly Salary
- Locality
- State

## Features

- Natural Language to SQL conversion
- SQLite database integration
- AI-powered SQL query execution
- Five saved training examples
- FastAPI REST API endpoint
- Swagger API documentation

## API Endpoint

POST /cia/sql-analyst

Request Body:

{
"question": "What is the average monthly salary across all job records?",
"conversation_id": "test-001"
}

## Running the Application

Activate the Python virtual environment.

Run:

python api.py

Open Swagger documentation:

http://127.0.0.1:8000/docs

## API Testing

The API was tested using Swagger UI.

Three API interactions were successfully tested:

1. Average monthly salary across all job records.
2. Top 5 states by number of job records.
3. Top 5 most common job titles.

All three requests returned HTTP 200 responses.

## Project Status

Vanna AI Text-to-SQL integration and FastAPI endpoint testing completed.
