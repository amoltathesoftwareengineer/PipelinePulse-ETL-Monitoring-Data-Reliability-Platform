
import json

import pytest

from src.history_store import save_run_history, load_run_history


def test_save_and_load_history(tmp_path):
    history_file = tmp_path / "pipeline_history.json"

    run = {
        "pipeline_name": "sales_etl",
        "status": "SUCCESS",
        "records_extracted": 100,
        "records_loaded": 95,
        "records_rejected": 5,
    }

    save_run_history(run, history_file)

    history = load_run_history(history_file)

    assert len(history) == 1
    assert history[0]["pipeline_name"] == "sales_etl"
    assert history[0]["records_loaded"] == 95


def test_multiple_runs_are_appended(tmp_path):
    history_file = tmp_path / "history.json"

    save_run_history({"status": "SUCCESS"}, history_file)
    save_run_history({"status": "FAILED"}, history_file)

    history = load_run_history(history_file)

    assert len(history) == 2
    assert history[0]["status"] == "SUCCESS"
    assert history[1]["status"] == "FAILED"


def test_missing_history_returns_empty_list(tmp_path):
    history_file = tmp_path / "missing.json"

    assert load_run_history(history_file) == []


def test_invalid_json_raises_error(tmp_path):
    history_file = tmp_path / "history.json"
    history_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_run_history(history_file)


def test_non_list_history_raises_error(tmp_path):
    history_file = tmp_path / "history.json"
    history_file.write_text(json.dumps({"status": "SUCCESS"}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_run_history(history_file)
