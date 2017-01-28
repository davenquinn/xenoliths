d3 = require 'd3'
require 'd3-selection-multi'
simplify = require 'simplify-js'
uuid = require 'uuid'

module.exports =
  # Builds the temperature profile from dz
  makeProfile: (row, simp=true)->
    profile = row.temperature.map (d,i)->
      {x: d, y: i*row.dz/1000}
    if simp
      profile=simplify(profile,0.005,true)
    return profile
  lithosphereDepth: (profile)->
    # Depth to the top of the mantle lithosphere
    for i in profile
      return i.z if i.T >= 1300
    return 91 # If it's too deep
  textPath: (lineGenerator)->
    f = (d,i)->
      el = d3.select @
      id = uuid.v4()
      el.append 'defs'
        .append 'path'
        .attrs
          id: id
          d: lineGenerator
      el.append 'use'
        .attrs 'xlink:href': "##{id}"
    (sel)->
      sel.each f
         .select 'use'
