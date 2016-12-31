module.exports =
  # Builds the temperature profile from dz
  makeProfile: (row)->
    row.temperature.map (d,i)->{x: d, y: i*row.dz/1000}
  lithosphereDepth: (profile)->
    # Depth to the top of the mantle lithosphere
    for i in profile
      return i.z if i.T >= 1300
    return 91 # If it's too deep

