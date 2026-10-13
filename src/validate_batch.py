
import sys
from pathlib import Path

import pandas as pd

# Locate the project root, even when this script is run
# from a different working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "sample_data.csv"

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "transaction_date",
]


def validate_batch(file_path):
    print("=" * 50)
    print("BATCH DATA QUALITY VALIDATION")
    print("=" * 50)

    # 1. Check whether the file exists.
    if not file_path.exists():
        print(f"FAILED: Data file not found: {file_path}")
        return False

    # 2. Load the batch.
    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        print(f"FAILED: Could not read CSV: {exc}")
        return False

    print(f"File: {file_path.name}")
    print(f"Records loaded: {len(df)}")

    errors = []

    # 3. Check required columns.
    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        print(f"FAILED: Missing columns: {missing_columns}")
        return False

    # 4. Check that the batch contains records.
    if df.empty:
        errors.append("The batch contains no records.")

    # 5. Check missing and blank values.
    for column in REQUIRED_COLUMNS:
        values = df[column]
        missing = values.isna()

        if pd.api.types.is_object_dtype(values.dtype):
            missing = missing | values.astype("string").str.strip().eq(
                ""
            ).fillna(False)

        count = int(missing.sum())

        if count:
            errors.append(
                f"{column}: {count} missing or blank values"
            )

    # 6. Check duplicate transaction IDs.
    ids = df["transaction_id"].astype("string").str.strip()
    valid_ids = ids.notna() & ids.ne("")

    duplicate_count = int(
        ids[valid_ids].duplicated().sum()
    )

    if duplicate_count:
        errors.append(
            f"Found {duplicate_count} duplicate transaction IDs"
        )

    # 7. Check numeric and positive transaction amounts.
    amounts = pd.to_numeric(df["amount"], errors="coerce")

    invalid_amounts = int(amounts.isna().sum())

    if invalid_amounts:
        errors.append(
            f"Found {invalid_amounts} non-numeric or missing amounts"
        )

    non_positive = int((amounts.notna() & (amounts <= 0)).sum())

    if non_positive:
        errors.append(
            f"Found {non_positive} amounts that are not positive"
        )

    # 8. Check transaction dates.
    dates = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
        format="mixed",
    )

    invalid_dates = int(dates.isna().sum())

    if invalid_dates:
        errors.append(
            f"Found {invalid_dates} invalid transaction dates"
        )

    # 9. Report the outcome.
    print("-" * 50)

    if errors:
        print("STATUS: FAILED")

        for error in errors:
            print(f"ERROR: {error}")

        print("The batch has been rejected.")
        print("Fix the errors and push your changes again.")
        return False

    print("STATUS: PASSED")
    print("All data quality checks passed.")
    print(f"Validated records: {len(df)}")
    print("The batch is ready for downstream processing.")

    return True


if __name__ == "__main__":
    success = validate_batch(DATA_FILE)
    sys.exit(0 if success else 1)
