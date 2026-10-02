# Technical Report — Design Before Execution

## Objective

Build a compact and auditable condition-monitoring workflow that demonstrates data ingestion, validation, SQL storage, KPI reporting, feature engineering, and baseline anomaly detection.

## Design decisions

- Use a chronological 70/30 split so future data never influences the reference period.
- Fit robust medians and median absolute deviations only on normal training records.
- Use a maximum multivariate robust z-score because it is transparent to engineering reviewers.
- Store the raw sensor values, labels, split, score, and prediction in SQLite for traceability.
- Keep the generated dataset explicitly synthetic and describe its assumptions.

## Limitations

- Synthetic anomalies are easier to detect than many real degradation modes.
- No maintenance work orders, environmental factors, or sensor calibration records exist.
- The global detector does not yet learn machine-specific or operating-state-specific baselines.
- Point-wise metrics do not measure event-level detection delay or alert persistence.
- The generated results demonstrate software engineering, not production readiness.

