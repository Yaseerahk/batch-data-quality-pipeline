
# Batch Data Quality CI/CD Pipeline

## Overview

An automated batch data validation pipeline built with Python,
Pandas, and GitHub Actions. It validates transaction data whenever
code is pushed to a branch or a pull request is opened.

## Architecture

1. A developer pushes changes to GitHub.
2. GitHub Actions triggers the workflow.
3. Python loads the CSV batch.
4. Data quality checks run against the records.
5. The pipeline passes if the data is valid or fails if errors
   are detected.

## Data Quality Checks

- Required columns and missing values
- Duplicate transaction IDs
- Numeric and positive transaction amounts
- Valid transaction dates
- Empty batches

## Technology Stack

- Python
- Pandas
- Git and GitHub
- GitHub Actions
- YAML

## How to Run Locally

Install dependencies:

    python -m pip install -r requirements.txt

Run the pipeline:

    python src/validate_batch.py

## Expected Outcome

Valid data produces a successful pipeline run.
Invalid data produces error messages and a non-zero exit code.

## Future Improvements

- Store validated records in PostgreSQL
- Generate data quality reports
- Add automated unit tests
- Track batch processing metrics
- Add data transformation and ingestion stages
