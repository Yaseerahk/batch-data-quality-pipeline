
import pandas as pd

from src.validate_batch import validate_batch


def create_batch(tmp_path, records):
    file_path = tmp_path / "test_batch.csv"
    pd.DataFrame(records).to_csv(file_path, index=False)
    return file_path


def valid_records():
    return [
        {
            "transaction_id": "1001",
            "customer_id": "C001",
            "amount": 250.50,
            "transaction_date": "2026-10-01",
        },
        {
            "transaction_id": "1002",
            "customer_id": "C002",
            "amount": 180.00,
            "transaction_date": "2026-10-02",
        },
    ]


def test_valid_batch_passes(tmp_path):
    file_path = create_batch(tmp_path, valid_records())

    assert validate_batch(file_path) is True


def test_duplicate_transaction_ids_fail(tmp_path):
    records = valid_records()
    records[1]["transaction_id"] = "1001"

    file_path = create_batch(tmp_path, records)

    assert validate_batch(file_path) is False


def test_negative_amount_fails(tmp_path):
    records = valid_records()
    records[0]["amount"] = -50

    file_path = create_batch(tmp_path, records)

    assert validate_batch(file_path) is False


def test_missing_customer_id_fails(tmp_path):
    records = valid_records()
    records[0]["customer_id"] = ""

    file_path = create_batch(tmp_path, records)

    assert validate_batch(file_path) is False
