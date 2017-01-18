SELECT
  r.name,
  r.type,
  r.subduction_time,
  r.underplating_duration,
  p.name profile_id,
  p.temperature,
  p.dz,
  p.time
FROM
thermal_modeling.model_profile p
JOIN thermal_modeling.model_run r
  ON r.id = p.run_id
WHERE r.name = ANY($1)
  AND p.name = $2
ORDER BY p.time DESC
