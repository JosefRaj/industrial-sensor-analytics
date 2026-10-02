"""Human-readable reporting and dependency-free SVG visualization."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd


def write_temperature_svg(frame: pd.DataFrame, path: Path) -> None:
    width, height, margin = 1000, 360, 55
    evaluation = frame.loc[frame["split"] == "evaluation"].copy()
    y_min, y_max = evaluation["temperature_c"].min() - 2, evaluation["temperature_c"].max() + 2
    x_values = evaluation["timestamp"].astype("int64").to_numpy(dtype=float)
    x_min, x_max = x_values.min(), x_values.max()

    def x_coord(value: float) -> float:
        return margin + (value - x_min) / (x_max - x_min) * (width - 2 * margin)

    def y_coord(value: float) -> float:
        return height - margin - (value - y_min) / (y_max - y_min) * (height - 2 * margin)

    colors = ["#005eb8", "#d1495b", "#2a9d8f", "#7b2cbf"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="#333"/>',
        f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="#333"/>',
        '<text x="500" y="28" text-anchor="middle" font-family="Arial" font-size="18">Evaluation-period temperature and detected alerts</text>',
    ]
    for index, (machine, group) in enumerate(evaluation.groupby("machine_id")):
        xs = group["timestamp"].astype("int64").to_numpy(dtype=float)
        ys = group["temperature_c"].to_numpy(dtype=float)
        points = " ".join(f"{x_coord(x):.1f},{y_coord(y):.1f}" for x, y in zip(xs, ys))
        color = colors[index % len(colors)]
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="1.5" points="{points}"/>')
        alerts = group.loc[group["anomaly_prediction"] == 1]
        for row in alerts.itertuples():
            parts.append(
                f'<circle cx="{x_coord(float(row.timestamp.value)):.1f}" cy="{y_coord(float(row.temperature_c)):.1f}" r="3" fill="#111"/>'
            )
        parts.append(
            f'<text x="{width-margin-80}" y="{margin+18*index}" fill="{color}" font-family="Arial" font-size="13">{html.escape(machine)}</text>'
        )
    parts.append(f'<text x="20" y="{height/2}" transform="rotate(-90 20 {height/2})" font-family="Arial" font-size="13">Temperature (°C)</text>')
    parts.append(f'<text x="{width/2}" y="{height-12}" text-anchor="middle" font-family="Arial" font-size="12">Time → (black dots: detected alerts)</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def write_summary(path: Path, quality: dict[str, object], metrics: dict[str, object], kpis: list[dict[str, object]], threshold: float) -> None:
    rows = "\n".join(
        f"| {item['machine_id']} | {item['samples']} | {item['avg_temperature_c']} | {item['max_temperature_c']} | {item['avg_vibration_mm_s']} | {item['flagged_samples']} |"
        for item in kpis
    )
    text = f"""# Generated Engineering Summary

## Scope

This report describes a reproducible software demonstration using synthetic rotating-equipment data. It is not a field study and does not represent an employer or customer deployment.

## Data quality

- Rows checked: {quality['row_count']}
- Simulated machines: {quality['machine_count']}
- Validation passed: {quality['passed']}
- Duplicate machine/timestamp keys: {quality['duplicate_keys']}
- Invalid physical ranges: {quality['range_violations']}

## Evaluation-period alert performance

- Robust-score threshold: {threshold:.2f}
- Accuracy: {metrics['accuracy']:.3f}
- Precision: {metrics['precision']:.3f}
- Recall/sensitivity: {metrics['recall']:.3f}
- Specificity: {metrics['specificity']:.3f}
- F1: {metrics['f1']:.3f}
- Confusion matrix `[[TN, FP], [FN, TP]]`: {metrics['confusion_matrix']}

These metrics measure recovery of deliberately injected synthetic events. They must not be generalized to real equipment.

## Machine KPIs from SQLite

| Machine | Samples | Avg temp °C | Max temp °C | Avg vibration mm/s | Flagged samples |
|---|---:|---:|---:|---:|---:|
{rows}

## Engineering interpretation

The detector is intentionally simple and transparent: it learns robust sensor medians and median absolute deviations only from the chronological training period, then flags evaluation readings when any sensor deviates strongly. This makes the alert logic easy to audit. Before real deployment, the main risks would be operating-state confounding, sensor drift, machine-specific baselines, alert persistence, and the cost of false positives. A production study would therefore require real labelled history, per-asset calibration, temporal cross-validation, and maintenance feedback.
"""
    path.write_text(text, encoding="utf-8")

