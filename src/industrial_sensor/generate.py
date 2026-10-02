"""Deterministic physics-inspired sensor-data generator."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_sensor_data(
    periods: int = 576,
    machine_count: int = 3,
    seed: int = 42,
) -> pd.DataFrame:
    """Return synthetic five-minute readings with labelled evaluation anomalies."""
    if periods < 120:
        raise ValueError("periods must be at least 120")
    if machine_count < 1:
        raise ValueError("machine_count must be positive")

    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2026-01-05", periods=periods, freq="5min", tz="UTC")
    rows: list[dict[str, object]] = []
    split_index = int(periods * 0.70)

    for machine_idx in range(machine_count):
        machine_id = f"M-{machine_idx + 1:02d}"
        phase = machine_idx * 0.7
        machine_offset = machine_idx * 0.8

        for idx, timestamp in enumerate(timestamps):
            minute_of_day = timestamp.hour * 60 + timestamp.minute
            daily_cycle = np.sin(2 * np.pi * minute_of_day / 1440 + phase)
            state_selector = (idx // 36 + machine_idx) % 5
            if state_selector == 0:
                state, load = "idle", 0.25
            elif state_selector in (3, 4):
                state, load = "high_load", 1.0
            else:
                state, load = "normal", 0.65

            temperature = 32 + 12 * load + 2.2 * daily_cycle + machine_offset + rng.normal(0, 0.45)
            vibration = 0.7 + 1.5 * load + 0.12 * machine_idx + rng.normal(0, 0.09)
            current = 3.5 + 8.2 * load + 0.2 * daily_cycle + rng.normal(0, 0.28)
            rpm = 1450 + 30 * load - 8 * machine_idx + rng.normal(0, 5.0)

            is_evaluation = idx >= split_index
            event_start = split_index + 24 + machine_idx * 31
            is_anomaly = is_evaluation and event_start <= idx < event_start + 10
            if is_anomaly:
                ramp = (idx - event_start + 1) / 10
                # Deliberately overlapping degradation signature: early points can
                # resemble ordinary load changes, which makes evaluation less trivial.
                temperature += 3.0 + 3.5 * ramp
                vibration += 0.30 + 0.45 * ramp
                current += 0.8 + 1.0 * ramp
                rpm -= 14 + 18 * ramp

            rows.append(
                {
                    "timestamp": timestamp,
                    "machine_id": machine_id,
                    "temperature_c": round(float(temperature), 3),
                    "vibration_mm_s": round(float(vibration), 4),
                    "current_a": round(float(current), 3),
                    "rpm": round(float(rpm), 2),
                    "operating_state": state,
                    "anomaly_label": int(is_anomaly),
                    "split": "evaluation" if is_evaluation else "train",
                }
            )

    return pd.DataFrame(rows).sort_values(["timestamp", "machine_id"]).reset_index(drop=True)
