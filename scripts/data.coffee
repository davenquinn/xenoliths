path = require "path"
fs = require "fs"

basename = (fn)->fn.substr 0, fn.lastIndexOf('.')
getProfile = (fn)->
  # Gets the vertical profile, zipping for friendliness
  p = require fn
  return p.z.map (d,i)->{T: p.T[i], z: d*0.001}

ml_depth = (profile)->
  # Find depth of the mantle lithosphere
  for i in profile
    return i.z if i.T >= 1300
  return 91 # If it's too deep

module.exports = (dir,cfg)->
  cfg.map (scenario)->
    # Builds each scenario from configuration
    unless scenario.id.constructor == Array
      scenario.id = [scenario.id]

    scenario.slices.forEach (d)->
      d.profile = scenario.id.map (id)->
        filename = path.join dir, id, d.id
        getProfile(filename).filter (a)-> a.z <= 91
      d.ml = ml_depth d.profile[0]
      console.log d.ml
    return scenario

