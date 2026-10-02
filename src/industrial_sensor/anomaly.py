"""Interpretable robust anomaly detector fit on normal training data only."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .features import SENSOR_COLUMNS


class RobustAnomalyDetector:
    """Score the largest absolute robust z-score across selected sensors."""

    def __init__(self, threshold: float = 6.0) -> None:
        self.threshold = float(threshold)
        self.medians: pd.Series | None = None
        self.scales: pd.Series | None = None

    def fit(self, frame: pd.DataFrame) -> "RobustAnomalyDetector":
        reference = frame.loc[frame["anomaly_label"] == 0, SENSOR_COLUMNS]
        if reference.empty:
            raise ValueError("normal reference data is required")
        self.medians = reference.median()
        mad = (reference - self.medians).abs().median()
        self.scales = (1.4826 * mad).clip(lower=1e-6)
        return self

    def score(self, frame: pd.DataFrame) -> np.ndarray:
        if self.medians is None or self.scales is None:
            raise RuntimeError("detector must be fitted before scoring")
        robust_z = ((frame[SENSOR_COLUMNS] - self.medians) / self.scales).abs()
        return robust_z.max(axis=1).to_numpy(dtype=float)

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        return (self.score(frame) >= self.threshold).astype(int)

