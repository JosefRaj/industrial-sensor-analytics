"""Feature engineering utilities."""

from __future__ import annotations

import pandas as pd


SENSOR_COLUMNS = ["temperature_c", "vibration_mm_s", "current_a", "rpm"]


def add_rolling_features(frame: pd.DataFrame, window: int = 12) -> pd.DataFrame:
    """Add per-machine one-hour rolling mean and standard deviation features."""
    if window < 2:
        raise ValueError("window must be at least 2")
    result = frame.sort_values(["machine_id", "timestamp"]).copy()
    grouped = result.groupby("machine_id", group_keys=False)
    for column in SENSOR_COLUMNS:
        result[f"{column}_rolling_mean"] = grouped[column].transform(
            lambda series: series.rolling(window, min_periods=1).mean()
        )
        result[f"{column}_rolling_std"] = grouped[column].transform(
            lambda series: series.rolling(window, min_periods=2).std().fillna(0.0)
        )
    return result.sort_values(["timestamp", "machine_id"]).reset_index(drop=True)

