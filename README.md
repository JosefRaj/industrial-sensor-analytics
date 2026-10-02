# Industrial Sensor Analytics — Draft Portfolio Project

This local portfolio draft demonstrates an end-to-end Python and SQL workflow for monitoring rotating industrial equipment. It generates a transparent physics-inspired **synthetic** dataset, validates data quality, stores clean records in SQLite, calculates operational KPIs, flags multivariate anomalies, and writes a concise engineering report.

The project is designed for working-student roles spanning data analysis, test engineering, electrical engineering support, technical documentation, and office-based engineering operations. It is a personal portfolio project, not employment history.

## Project origin and ownership

This project was developed independently as a portfolio extension of verified coursework and laboratory exposure in electrical measurements, electronics, microcomputers, signal processing, and machine learning. It was **not** an official graded laboratory assignment, university research job, employer project, or factory deployment.

Interview-safe description: **“I built this independently to connect my electrical-measurement and machine-learning coursework with an auditable Python/SQL workflow for industrial sensor data.”**

## What it demonstrates

- reproducible time-series data generation with documented assumptions;
- validation of schema, timestamps, missing values, duplicates, and physical ranges;
- Python/Pandas cleaning and rolling feature engineering;
- SQLite schema, indexes, parameterized loading, and KPI queries;
- interpretable anomaly scoring using training-only robust statistics;
- precision, recall, F1, specificity, and confusion-matrix reporting on known injected events;
- an SVG time-series overview and a non-ML stakeholder summary;
- automated tests for data generation, validation, leakage control, and pipeline outputs.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
python -m unittest discover -s tests -v
```

Generated artifacts are written to `reports/generated/`. The random seed, thresholds, and train/evaluation time boundary are saved with the output.

## Data honesty

All records are generated locally. They do not represent a real plant, customer, employer, machine, or measured field deployment. The labels indicate anomalies deliberately injected by the generator so that the engineering pipeline can be tested and discussed transparently.

## Repository layout

```text
data/README.md
sql/schema.sql
sql/analysis_queries.sql
src/industrial_sensor/
scripts/run_pipeline.py
tests/test_pipeline.py
reports/technical_report.md
```

## CV status

The repository can support a personal-project bullet after Yousef has reviewed the code and can explain the decisions. It must never be presented as paid work or a deployed industrial system. GitHub publication is pending explicit approval.
