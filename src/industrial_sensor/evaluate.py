"""Binary alert metrics without an external ML dependency."""

from __future__ import annotations

import numpy as np


def binary_metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, object]:
    y = np.asarray(labels, dtype=int)
    p = np.asarray(predictions, dtype=int)
    if y.shape != p.shape or y.ndim != 1:
        raise ValueError("labels and predictions must be one-dimensional and equal length")
    tn = int(np.sum((y == 0) & (p == 0)))
    fp = int(np.sum((y == 0) & (p == 1)))
    fn = int(np.sum((y == 1) & (p == 0)))
    tp = int(np.sum((y == 1) & (p == 1)))

    def safe_div(numerator: int, denominator: int) -> float:
        return float(numerator / denominator) if denominator else 0.0

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    return {
        "accuracy": safe_div(tp + tn, len(y)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe_div(2 * precision * recall, precision + recall),
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "support": int(len(y)),
    }

