
import sys
from pathlib import Path

import pandas as pd

DATA_FILE = Path("data/sample_data.csv")

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "transaction_date",
]


def validate_batch(file_path):
    print(f"Starting batch validation: {file_path}")

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return False

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        print(f"ERROR: Could not read CSV: {exc}")
        return False

    errors = []

    # Check required columns
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        errors.append(
            f"Missing columns: {sorted(missing_columns)}"
        )
        print("\n".join(errors))
        return False

    print(f"Records loaded: {len(df)}")

    if df.empty:
        errors.append("Batch contains no records.")

    # Check missing values
    for column in REQUIRED_COLUMNS:
        missing = int(df[column].isna().sum())

        if missing > 0:
            errors.append(
                f"{column}: {missing} missing values"
            )

    # Check duplicate transaction IDs
    duplicates = int(
        df["transaction_id"].duplicated().sum()
    )

    if duplicates > 0:
        errors.append(
            f"Found {duplicates} duplicate transaction IDs"
        )

    # Check numeric amounts
    amounts = pd.to_numeric(df["amount"], errors="coerce")

    invalid_amounts = int(amounts.isna().sum())

    if invalid_amounts > 0:
        errors.append(
            f"Found {invalid_amounts} invalid amounts"
        )

    elif (amounts <= 0).any():
        errors.append("Transaction amounts must be positive.")

    # Check transaction dates
    dates = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )

    invalid_dates = int(dates.isna().sum())

    if invalid_dates > 0:
        errors.append(
            f"Found {invalid_dates} invalid transaction dates"
        )

    # Report results
    if errors:
        print("\nBATCH VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        print("Pipeline stopped. Fix the errors and retry.")
        return False

    print("BATCH VALIDATION PASSED")
    print(f"Validated records: {len(df)}")
    print("Batch is ready for downstream processing.")

    return True


if __name__ == "__main__":
    success = validate_batch(DATA_FILE)
    sys.exit(0 if success else 1)
