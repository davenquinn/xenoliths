_ = require 'underscore'
d3 = require 'd3'

modelColors = require '../shared/colors'

module.exports = (ax)->

  gen = ax.line().interpolate('basis')
  line = (key)->
    (d)-> gen _.zip(d.time, d[key])

  agen = d3.svg.area()
    .x (d)->ax.scale.x d[0]
    .y0 (d)->ax.scale.y d[1]
    .y1 (d)->ax.scale.y d[2]

  area = (d)->
    agen _.zip(d.time, d['lower'], d['upper'])

  (enter)->
    enter.append 'path'
      .attr
        fill: (d)->modelColors(d).alpha(0.2).css()
        d: area

    enter.append 'path'
      .attr
        class: 'tracer'
        stroke: (d)->modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: line('upper')
        "stroke-dasharray": '5,1'

    enter.append 'path'
      .attr
        class: 'tracer'
        stroke: (d)->modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: line('lower')

