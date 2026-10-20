
# 🚦 PipelinePulse — ETL Monitoring & Data Reliability Platform

PipelinePulse is a Python-based ETL monitoring project that tracks pipeline execution status, processing duration, record counts, data validation failures, and execution history.

## 🚀 Features

- Extract, transform, and load workflow execution
- Required-field data validation
- Accepted and rejected record tracking
- Pipeline success and failure status
- Execution duration measurement
- JSON-based pipeline execution history
- Automated tests with pytest
- GitHub Actions CI workflow

## 🧰 Technology Stack

- Python 3.12+
- SQL
- PostgreSQL sample-query integration (planned)
- pytest
- JSON
- GitHub Actions

## 📂 Project Structure

```text
PipelinePulse-ETL-Monitoring-Data-Reliability-Platform/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── src/
│   ├── pipeline_monitor.py
│   └── history_store.py
├── tests/
│   ├── test_pipeline_monitor.py
│   └── test_history_store.py
├── reports/
│   └── pipeline_history.json  # Created when history is saved
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/amoltathesoftwareengineer/PipelinePulse-ETL-Monitoring-Data-Reliability-Platform.git
cd PipelinePulse-ETL-Monitoring-Data-Reliability-Platform

python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies and run tests:

```bash
pip install -r requirements.txt
python -m pytest -v
```

## 💻 Usage

```python
from src.pipeline_monitor import run_pipeline
from src.history_store import save_run_history, load_run_history

source_data = [
    {"id": 1, "name": "Amit"},
    {"id": 2, "name": "Priya"},
    {"id": 3, "name": None},
]

loaded_records = []

result = run_pipeline(
    name="employee_pipeline",
    extract=lambda: source_data,
    transform=lambda rows: rows,
    load=lambda rows: loaded_records.extend(rows),
    required_fields=["id", "name"],
)

save_run_history(result)

print("Status:", result["status"])
print("Extracted:", result["records_extracted"])
print("Loaded:", result["records_loaded"])
print("Rejected:", result["records_rejected"])
print("Duration:", result["duration_seconds"])

history = load_run_history()
print("Total recorded runs:", len(history))
```

Run the example from the repository root directory.

## 📊 Monitoring Metrics

| Metric | Description |
|---|---|
| Pipeline status | SUCCESS or FAILED |
| Execution duration | Elapsed processing time in seconds |
| Records extracted | Number of records returned by extraction |
| Records loaded | Number of accepted records passed to the load function |
| Records rejected | Number of records failing required-field validation |
| Error summary | Exception details for failed pipeline stages |
| Run history | Previously saved execution results in JSON |

## 🧪 Testing

Tests cover:

- Required-field validation
- Accepted and rejected records
- Successful pipeline execution
- Pipeline failure logging
- Execution metrics
- Saving and loading history
- Invalid history-file handling

Run tests locally using:

```bash
python -m pytest -v
```

GitHub Actions runs the test suite on pushes and pull requests.

## ⚠️ Limitations

- Extraction and loading are supplied as Python callables.
- PostgreSQL connectivity and scheduled ETL orchestration are not implemented.
- History is stored in a local JSON file rather than a centralized monitoring database.
- A Streamlit dashboard and alerting system are future enhancements.
- Execution duration measures the Python pipeline call, not a separate database performance benchmark.

## 🗺️ Roadmap

- [x] ETL pipeline execution wrapper
- [x] Required-field validation
- [x] Success and failure tracking
- [x] Processing duration and record metrics
- [x] JSON execution history
- [x] Automated tests
- [x] GitHub Actions workflow
- [ ] PostgreSQL metadata storage
- [ ] Scheduled pipeline execution
- [ ] Interactive Streamlit monitoring dashboard
- [ ] Alerts for pipeline failures and data quality issues

## 🔐 Data Reliability and Safety

- Validate records before loading.
- Keep database credentials out of source control.
- Avoid logging sensitive record contents.
- Use transactions when integrating a real database.
- Test recovery and retry behavior before production use.

## 📄 License

MIT License. See the [LICENSE](LICENSE) file if included in the repository.
