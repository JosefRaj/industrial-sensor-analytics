"""SQLite persistence and KPI querying."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def write_database(frame: pd.DataFrame, database_path: Path, schema_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists():
        database_path.unlink()
    serializable = frame.copy()
    serializable["timestamp"] = serializable["timestamp"].astype(str)
    columns = [
        "timestamp", "machine_id", "temperature_c", "vibration_mm_s", "current_a", "rpm",
        "operating_state", "anomaly_label", "split", "anomaly_score", "anomaly_prediction",
    ]
    with sqlite3.connect(database_path) as connection:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        serializable[columns].to_sql("sensor_readings", connection, if_exists="append", index=False)


def machine_kpis(database_path: Path) -> list[dict[str, object]]:
    query = """
        SELECT machine_id, COUNT(*) AS samples,
               ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
               ROUND(MAX(temperature_c), 2) AS max_temperature_c,
               ROUND(AVG(vibration_mm_s), 3) AS avg_vibration_mm_s,
               SUM(anomaly_prediction) AS flagged_samples
        FROM sensor_readings GROUP BY machine_id ORDER BY machine_id
    """
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(query).fetchall()]

