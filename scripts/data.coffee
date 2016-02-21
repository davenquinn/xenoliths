q = require "../shared/query"

ml_depth = (profile)->
  # Find depth of the mantle lithosphere
  for i in profile
    return i.z if i.T >= 1300
  return 91 # If it's too deep

getProfile = (scenario_id, slice_id)->
  console.log scenario_id, slice_id
  sql = "SELECT
    	p.name,
    	p.temperature,
    	p.dz,
    	p.time
  	FROM
  	thermal_modeling.model_profile p
  	JOIN thermal_modeling.model_run r
  		ON r.id = p.run_id
  	WHERE r.name = %1::text
      AND p.name = %2::text;"
  q sql, [scenario_id, slice_id], (err, d)->
    console.log d

module.exports = (cfg)->
  # Return configuration for all scenarios
  cfg.map (scenario)->
    # Builds each scenario from configuration
    unless scenario.id.constructor == Array
      scenario.id = [scenario.id]

    scenario.slices.forEach (d)->
      d.profile = scenario.id.map (scenario_id)->
        getProfile(scenario_id, d.id)
        return 1

      d.ml = ml_depth d.profile[0]
      console.log d.ml
    return scenario
