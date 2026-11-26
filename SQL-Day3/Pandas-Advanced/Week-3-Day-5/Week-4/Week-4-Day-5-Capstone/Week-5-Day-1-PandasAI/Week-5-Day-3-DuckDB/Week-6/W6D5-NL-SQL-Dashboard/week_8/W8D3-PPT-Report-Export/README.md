# Week 8 Day 3 – PPT Report Export

## Objective

Automate executive summary generation and PowerPoint report export using Python and AI.

## Tools Used

- Python
- Pandas
- Matplotlib
- python-pptx
- FastAPI
- Ollama (qwen2.5:3b)
- Groq (openai/gpt-oss-20b)

## Implementation

- CSV upload and data validation
- Exploratory Data Analysis (EDA)
- AI-powered executive summary generation
- Python-based percentage calculation
- Automated PowerPoint report generation
- AI summary integration into speaker notes
- CIA API report download

## Datasets

- job_market_india.csv
- crm_data.csv

## Validation Results

- Job market report: 7 slides
- CRM report: 7 slides
- CRM records: 100
- Total deal value: INR 24,875,000
- Verified top-three share: 59.84%
- CSV upload: PASS
- EDA generation: PASS
- AI summary generation: PASS
- PPT export and download: PASS
- Speaker notes integration: PASS

## Known Limitations

- AI summary contains 238 words instead of approximately 200.
- AI-generated business terminology requires review.
- CIA API currently supports CRM-specific CSV columns.
- Visual slide layout requires manual verification.

## Conclusion

The end-to-end workflow from CSV upload to AI summary generation and PowerPoint download was successfully tested.
