WITH
  a AS (
    SELECT
      array_agg(p.time ORDER BY p.time DESC) AS profile_time,
      p.run_id AS id
    FROM thermal_modeling.model_profile p
    JOIN thermal_modeling.model_run r ON p.run_id = r.id
    GROUP BY p.run_id),
  b AS (
    SELECT
      min(t.temperature) AS min_temp,
      max(t.temperature) AS max_temp,
      array_agg(t.temperature ORDER BY t.time DESC) AS temperature,
      array_agg(t.time ORDER BY t.time DESC) AS time,
      array_agg(t.time = ANY(a.profile_time) ORDER BY t.time DESC) AS profile_time,
      t.final_depth AS depth,
      t.run_id AS id
    FROM thermal_modeling.model_tracer t
    JOIN thermal_modeling.model_run r ON t.run_id = r.id
    JOIN a ON a.id = r.id
    WHERE r.type LIKE $1::text || '%'
      AND r.name != 'forearc-28-2'
      AND r.name != 'forearc-80-60'
    GROUP BY t.run_id, r.name, t.final_depth, a.profile_time),
  u AS (SELECT * FROM b WHERE b.depth = 40),
  l AS (SELECT * FROM b WHERE b.depth = 75)
SELECT
  r.*,
  u.time,
  u.profile_time profile,
  array[u.min_temp,l.max_temp] trange,
  u.temperature upper,
  l.temperature lower
FROM u
JOIN l ON u.id = l.id
JOIN thermal_modeling.model_run r ON u.id = r.id

