d3 = require "d3"

class Ternary
  constructor: (opts)->
    for k,v of opts
      @[k] = v
    @rescale @range
    @height = Math.sqrt 1-(1/4)
    @margin = [0,0] unless @margin

  point: (coords) =>
    sum = d3.sum coords
    if sum is 0
      return [0,0]
    else
      norm = coords.map (d)=>d/sum
      return [
        @margin[0]+@scale norm[1] + norm[2]/2
        @margin[1]+@scale @height*norm[0] + @height*norm[1]
      ]

  rescale: (@range) =>
    @range = [0,1] unless @range
    @scale = d3.scale.linear()
      .domain [0,1]
      .range @range

  line: (coordsList) =>
    interpolator = "linear" unless interpolator
    accessor = (d)->d unless accessor

    path = d3.svg.line()
      .x (d)->d[0]
      .y (d)->d[1]
      .interpolate interpolator

    positions = coordsList.map (d) => @point d
    path positions

  rule: (value, axis) =>
    if axis is 0
      ends = [
        [value,0,100-value]
        [value,100-value,0]
      ]
    else if axis is 1
      ends = [
        [0,value,100-value]
        [100-value,value,0]
      ]
    else if axis is 2
      ends = [
        [0, 100-value,value]
        [100-value,0,value]
      ]
    @line ends

  getValues: (pos) -> #NOTE! haven't checked if this works yet
    pos = pos.map @scale.inverse
    c = 1-pos[1]
    b = pos[0]-c/2
    a = y-b
    [a,b,c]

module.exports = Ternary
