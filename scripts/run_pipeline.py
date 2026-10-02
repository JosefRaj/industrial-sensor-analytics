"""Run the complete reproducible synthetic analytics workflow."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from industrial_sensor.anomaly import RobustAnomalyDetector
from industrial_sensor.database import machine_kpis, write_database
from industrial_sensor.evaluate import binary_metrics
from industrial_sensor.features import add_rolling_features
from industrial_sensor.generate import generate_sensor_data
from industrial_sensor.report import write_summary, write_temperature_svg
from industrial_sensor.validate import validate_sensor_data


def main() -> None:
    output = ROOT / "reports" / "generated"
    output.mkdir(parents=True, exist_ok=True)

    frame = generate_sensor_data(seed=42)
    quality = validate_sensor_data(frame)
    if not quality["passed"]:
        raise RuntimeError(f"data-quality validation failed: {quality}")

    frame = add_rolling_features(frame)
    training = frame.loc[frame["split"] == "train"]
    evaluation = frame.loc[frame["split"] == "evaluation"].copy()
    detector = RobustAnomalyDetector(threshold=2.0).fit(training)
    frame["anomaly_score"] = detector.score(frame)
    frame["anomaly_prediction"] = detector.predict(frame)
    evaluation = frame.loc[frame["split"] == "evaluation"]
    metrics = binary_metrics(evaluation["anomaly_label"].to_numpy(), evaluation["anomaly_prediction"].to_numpy())

    frame.to_csv(output / "synthetic_sensor_readings.csv", index=False)
    (output / "quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    configuration = {
        "seed": 42,
        "sampling_interval_minutes": 5,
        "training_fraction": 0.70,
        "detector": "maximum absolute robust z-score",
        "threshold": detector.threshold,
        "data_source": "physics-inspired synthetic generator",
    }
    (output / "run_config.json").write_text(json.dumps(configuration, indent=2), encoding="utf-8")

    database_path = output / "sensor_analytics.sqlite"
    write_database(frame, database_path, ROOT / "sql" / "schema.sql")
    kpis = machine_kpis(database_path)
    write_temperature_svg(frame, output / "temperature_alerts.svg")
    write_summary(output / "engineering_summary.md", quality, metrics, kpis, detector.threshold)
    print(json.dumps({"quality": quality, "metrics": metrics, "outputs": str(output)}, indent=2))


if __name__ == "__main__":
    main()
