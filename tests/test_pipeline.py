from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from industrial_sensor.anomaly import RobustAnomalyDetector
from industrial_sensor.generate import generate_sensor_data
from industrial_sensor.validate import validate_sensor_data


class SensorPipelineTests(unittest.TestCase):
    def test_generation_is_reproducible(self) -> None:
        first = generate_sensor_data(periods=144, machine_count=2, seed=7)
        second = generate_sensor_data(periods=144, machine_count=2, seed=7)
        self.assertTrue(first.equals(second))

    def test_validation_passes_generated_data(self) -> None:
        quality = validate_sensor_data(generate_sensor_data(periods=144, machine_count=2))
        self.assertTrue(quality["passed"])
        self.assertEqual(quality["duplicate_keys"], 0)

    def test_anomalies_exist_only_in_evaluation(self) -> None:
        frame = generate_sensor_data(periods=240, machine_count=2)
        self.assertEqual(int(frame.loc[frame["split"] == "train", "anomaly_label"].sum()), 0)
        self.assertGreater(int(frame.loc[frame["split"] == "evaluation", "anomaly_label"].sum()), 0)

    def test_detector_fits_training_partition_only(self) -> None:
        frame = generate_sensor_data(periods=240, machine_count=2)
        training = frame.loc[frame["split"] == "train"]
        evaluation = frame.loc[frame["split"] == "evaluation"]
        detector = RobustAnomalyDetector(threshold=2.0).fit(training)
        scores = detector.score(evaluation)
        self.assertTrue(np.isfinite(scores).all())
        self.assertEqual(len(scores), len(evaluation))

    def test_full_pipeline_writes_expected_outputs(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_pipeline.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('"quality"', result.stdout)
        generated = ROOT / "reports" / "generated"
        for name in [
            "synthetic_sensor_readings.csv", "quality_report.json", "metrics.json",
            "run_config.json", "sensor_analytics.sqlite", "temperature_alerts.svg",
            "engineering_summary.md",
        ]:
            self.assertTrue((generated / name).exists(), name)
        metrics = json.loads((generated / "metrics.json").read_text(encoding="utf-8"))
        self.assertGreater(metrics["recall"], 0.5)
        self.assertLess(metrics["recall"], 1.0)


if __name__ == "__main__":
    unittest.main()
