
from datetime import datetime, timezone
from time import perf_counter


def validate_records(records, required_fields=None):
    """Validate records and return accepted and rejected records."""
    required_fields = required_fields or []
    accepted = []
    rejected = []

    for index, record in enumerate(records):
        errors = []

        if not isinstance(record, dict):
            errors.append("Record must be a dictionary.")
        else:
            for field in required_fields:
                if field not in record or record[field] is None:
                    errors.append(f"Missing required field: {field}")

        if errors:
            rejected.append({
                "row_number": index + 1,
                "record": record,
                "errors": errors,
            })
        else:
            accepted.append(record)

    return accepted, rejected


def run_pipeline(name, extract, transform, load, required_fields=None):
    """Run ETL stages and return execution metrics."""
    started_at = datetime.now(timezone.utc)
    timer = perf_counter()

    result = {
        "pipeline_name": name,
        "status": "SUCCESS",
        "started_at": started_at.isoformat(),
        "ended_at": None,
        "duration_seconds": 0.0,
        "records_extracted": 0,
        "records_loaded": 0,
        "records_rejected": 0,
        "errors": [],
        "rejected_records": [],
    }

    try:
        source_records = list(extract())
        result["records_extracted"] = len(source_records)

        transformed_records = list(transform(source_records))
        accepted, rejected = validate_records(
            transformed_records, required_fields
        )

        result["records_rejected"] = len(rejected)
        result["rejected_records"] = rejected

        load(accepted)
        result["records_loaded"] = len(accepted)

    except Exception as exc:
        result["status"] = "FAILED"
        result["errors"].append(
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        result["duration_seconds"] = round(
            perf_counter() - timer, 6
        )
        result["ended_at"] = datetime.now(timezone.utc).isoformat()

    return result
