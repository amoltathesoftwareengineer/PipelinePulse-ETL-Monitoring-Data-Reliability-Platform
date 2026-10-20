
import json
from pathlib import Path


def save_run_history(run_result, file_path="reports/pipeline_history.json"):
    """Append one pipeline run result to a JSON history file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    history = []

    if path.exists():
        try:
            history = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("History file contains invalid JSON.") from exc

    if not isinstance(history, list):
        raise ValueError("History file must contain a JSON list.")

    history.append(run_result)

    path.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return str(path)


def load_run_history(file_path="reports/pipeline_history.json"):
    """Load previously saved pipeline runs."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        history = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("History file contains invalid JSON.") from exc

    if not isinstance(history, list):
        raise ValueError("History file must contain a JSON list.")

    return history
