# Generated Engineering Summary

## Scope

This report describes a reproducible software demonstration using synthetic rotating-equipment data. It is not a field study and does not represent an employer or customer deployment.

## Data quality

- Rows checked: 1728
- Simulated machines: 3
- Validation passed: True
- Duplicate machine/timestamp keys: 0
- Invalid physical ranges: {}

## Evaluation-period alert performance

- Robust-score threshold: 2.00
- Accuracy: 0.946
- Precision: 0.531
- Recall/sensitivity: 0.567
- Specificity: 0.969
- F1: 0.548
- Confusion matrix `[[TN, FP], [FN, TP]]`: [[474, 15], [13, 17]]

These metrics measure recovery of deliberately injected synthetic events. They must not be generalized to real equipment.

## Machine KPIs from SQLite

| Machine | Samples | Avg temp °C | Max temp °C | Avg vibration mm/s | Flagged samples |
|---|---:|---:|---:|---:|---:|
| M-01 | 576 | 40.24 | 47.18 | 1.728 | 46 |
| M-02 | 576 | 41.38 | 49.15 | 1.893 | 11 |
| M-03 | 576 | 42.18 | 48.3 | 2.009 | 30 |

## Engineering interpretation

The detector is intentionally simple and transparent: it learns robust sensor medians and median absolute deviations only from the chronological training period, then flags evaluation readings when any sensor deviates strongly. This makes the alert logic easy to audit. Before real deployment, the main risks would be operating-state confounding, sensor drift, machine-specific baselines, alert persistence, and the cost of false positives. A production study would therefore require real labelled history, per-asset calibration, temporal cross-validation, and maintenance feedback.
