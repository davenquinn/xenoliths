SELECT
  dz, heat_flow, temperature
FROM thermal_modeling.static_profile
ORDER BY temperature[50] DESC
