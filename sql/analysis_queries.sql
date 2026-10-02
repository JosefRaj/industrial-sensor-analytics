-- Machine-level operating KPIs
SELECT
    machine_id,
    COUNT(*) AS samples,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(MAX(temperature_c), 2) AS max_temperature_c,
    ROUND(AVG(vibration_mm_s), 3) AS avg_vibration_mm_s,
    ROUND(AVG(current_a), 2) AS avg_current_a,
    SUM(anomaly_prediction) AS flagged_samples
FROM sensor_readings
GROUP BY machine_id
ORDER BY machine_id;

-- Evaluation-period alert windows for engineering review
SELECT timestamp, machine_id, temperature_c, vibration_mm_s,
       current_a, rpm, anomaly_score
FROM sensor_readings
WHERE split = 'evaluation' AND anomaly_prediction = 1
ORDER BY timestamp, machine_id;

-- Daily workload and condition overview
SELECT
    SUBSTR(timestamp, 1, 10) AS day,
    machine_id,
    SUM(CASE WHEN operating_state = 'high_load' THEN 1 ELSE 0 END) AS high_load_samples,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(MAX(vibration_mm_s), 3) AS peak_vibration_mm_s
FROM sensor_readings
GROUP BY day, machine_id
ORDER BY day, machine_id;

