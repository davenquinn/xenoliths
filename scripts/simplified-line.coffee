d3 = require 'd3'
simplify = require 'simplify-js'

module.exports = (scales, amount=1)->
  """
  Takes scales object with {temp,depth}
  """
  line = d3.svg.line()
    .x (d)->d.x
    .y (d)->d.y

  (data)->
    d = data.map (d)->
      {
        x: scales.temp d.T
        y: scales.depth d.z
      }
    l = simplify d,amount,true
    line l

