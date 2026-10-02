# Data documentation

The pipeline creates a deterministic synthetic dataset for three rotating machines sampled every five minutes.

Columns:

- `timestamp`: UTC timestamp;
- `machine_id`: anonymous simulated asset identifier;
- `temperature_c`: winding/housing temperature proxy;
- `vibration_mm_s`: overall vibration-velocity proxy;
- `current_a`: motor-current proxy;
- `rpm`: shaft-speed proxy;
- `operating_state`: `idle`, `normal`, or `high_load`;
- `anomaly_label`: 1 only for an injected anomalous interval;
- `split`: chronological `train` or `evaluation` partition.

Normal signals contain daily cycles, machine-specific offsets, load-state effects, correlated variables, and seeded measurement noise. Evaluation anomalies combine temperature rise, vibration increase, excess current, and speed reduction. The generator is intended for software validation and portfolio discussion—not for scientific conclusions about real equipment.

