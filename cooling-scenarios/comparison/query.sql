SELECT
    r.*,
    p.name profile_id,
    p.temperature,
    p.dz
  FROM
  thermal_modeling.model_profile p
  JOIN thermal_modeling.model_run r
    ON r.id = p.run_id
  WHERE p.name = 'final'
    AND r.name != 'forearc-28-2'
