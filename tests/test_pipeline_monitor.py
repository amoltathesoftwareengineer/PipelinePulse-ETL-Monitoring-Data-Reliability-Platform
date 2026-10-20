
from src.pipeline_monitor import validate_records, run_pipeline


def test_valid_records_are_accepted():
    records = [
        {"id": 1, "name": "Amit"},
        {"id": 2, "name": "Priya"},
    ]

    accepted, rejected = validate_records(
        records, required_fields=["id", "name"]
    )

    assert len(accepted) == 2
    assert len(rejected) == 0


def test_missing_required_field_is_rejected():
    records = [
        {"id": 1, "name": "Amit"},
        {"id": 2, "name": None},
    ]

    accepted, rejected = validate_records(
        records, required_fields=["id", "name"]
    )

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert "Missing required field: name" in rejected[0]["errors"]


def test_pipeline_success_metrics():
    loaded = []

    result = run_pipeline(
        name="employee_pipeline",
        extract=lambda: [{"id": 1}, {"id": 2}],
        transform=lambda rows: rows,
        load=lambda rows: loaded.extend(rows),
        required_fields=["id"],
    )

    assert result["status"] == "SUCCESS"
    assert result["records_extracted"] == 2
    assert result["records_loaded"] == 2
    assert result["records_rejected"] == 0
    assert result["duration_seconds"] >= 0
    assert len(loaded) == 2


def test_pipeline_failure_is_recorded():
    result = run_pipeline(
        name="failing_pipeline",
        extract=lambda: (_ for _ in ()).throw(
            RuntimeError("Source unavailable")
        ),
        transform=lambda rows: rows,
        load=lambda rows: None,
    )

    assert result["status"] == "FAILED"
    assert len(result["errors"]) == 1
    assert "Source unavailable" in result["errors"][0]


def test_pipeline_tracks_rejected_records():
    result = run_pipeline(
        name="quality_pipeline",
        extract=lambda: [
            {"id": 1, "name": "Amit"},
            {"id": 2, "name": None},
        ],
        transform=lambda rows: rows,
        load=lambda rows: None,
        required_fields=["id", "name"],
    )

    assert result["records_extracted"] == 2
    assert result["records_loaded"] == 1
    assert result["records_rejected"] == 1
