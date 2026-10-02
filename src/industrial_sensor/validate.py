"""Dataset quality checks with machine-readable findings."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "timestamp",
    "machine_id",
    "temperature_c",
    "vibration_mm_s",
    "current_a",
    "rpm",
    "operating_state",
    "anomaly_label",
    "split",
}

RANGES = {
    "temperature_c": (-20.0, 150.0),
    "vibration_mm_s": (0.0, 30.0),
    "current_a": (0.0, 100.0),
    "rpm": (0.0, 10000.0),
}


def validate_sensor_data(frame: pd.DataFrame) -> dict[str, object]:
    missing_columns = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    if missing_columns:
        raise ValueError(f"missing required columns: {missing_columns}")

    missing_values = {name: int(value) for name, value in frame.isna().sum().items() if value}
    duplicate_keys = int(frame.duplicated(["timestamp", "machine_id"]).sum())
    range_violations = {
        column: int((~frame[column].between(low, high)).sum())
        for column, (low, high) in RANGES.items()
    }
    range_violations = {name: count for name, count in range_violations.items() if count}
    invalid_states = int((~frame["operating_state"].isin(["idle", "normal", "high_load"])).sum())
    invalid_splits = int((~frame["split"].isin(["train", "evaluation"])).sum())
    timestamp_order_violations = 0
    for _, group in frame.groupby("machine_id", sort=False):
        timestamp_order_violations += int((group["timestamp"].diff().dropna() <= pd.Timedelta(0)).sum())

    passed = not any(
        [missing_values, duplicate_keys, range_violations, invalid_states, invalid_splits, timestamp_order_violations]
    )
    return {
        "passed": bool(passed),
        "row_count": int(len(frame)),
        "machine_count": int(frame["machine_id"].nunique()),
        "missing_values": missing_values,
        "duplicate_keys": duplicate_keys,
        "range_violations": range_violations,
        "invalid_states": invalid_states,
        "invalid_splits": invalid_splits,
        "timestamp_order_violations": timestamp_order_violations,
    }

