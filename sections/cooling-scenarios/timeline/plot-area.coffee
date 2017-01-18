_ = require 'underscore'
d3 = require 'd3'
require 'd3-selection-multi'

modelColors = require '../shared/colors'

module.exports = (ax)->

  gen = ax.line().curve d3.curveBasis
  line = (key)->
    (d)-> gen _.zip(d.time, d[key])

  agen = d3.area()
    .x (d)->ax.scale.x d[0]
    .y0 (d)->ax.scale.y d[1]
    .y1 (d)->ax.scale.y d[2]

  area = (d)->
    agen _.zip(d.time, d['lower'], d['upper'])

  (d)->
    el = d3.select @
    el.append 'path'
      .datum d
      .attrs
        fill: modelColors(d).alpha(0.08).css()
        d: area

    el.append 'path'
      .datum d
      .attrs
        class: 'tracer'
        stroke: modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: line('upper')
        "stroke-dasharray": '5,1'

    el.append 'path'
      .datum d
      .attrs
        class: 'tracer'
        stroke: modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: line('lower')

