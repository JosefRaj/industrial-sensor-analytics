CREATE TABLE IF NOT EXISTS sensor_readings (
    timestamp TEXT NOT NULL,
    machine_id TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    vibration_mm_s REAL NOT NULL,
    current_a REAL NOT NULL,
    rpm REAL NOT NULL,
    operating_state TEXT NOT NULL,
    anomaly_label INTEGER NOT NULL CHECK (anomaly_label IN (0, 1)),
    split TEXT NOT NULL CHECK (split IN ('train', 'evaluation')),
    anomaly_score REAL NOT NULL,
    anomaly_prediction INTEGER NOT NULL CHECK (anomaly_prediction IN (0, 1)),
    PRIMARY KEY (timestamp, machine_id)
);

CREATE INDEX IF NOT EXISTS idx_readings_machine_time
ON sensor_readings(machine_id, timestamp);

CREATE INDEX IF NOT EXISTS idx_readings_split_prediction
ON sensor_readings(split, anomaly_prediction);

