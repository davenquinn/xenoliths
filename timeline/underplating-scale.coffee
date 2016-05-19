d3 = require 'd3'

module.exports = (ax)->

  s = d3.scale.linear()
    .domain [0,6]
    .range [ax.scale.x(24),ax.scale.x(24-6)]

  uScale = d3.svg.axis()
    .scale s
    .ticks(4)
    .tickSize -3
    .orient 'top'

  labelText = null

  F = (el)->
    el.attr
        class: 'u-scale'
        transform: 'translate(0,-5)'
      .call uScale

    c = '#888888'
    el.select '.domain'
      .attr
        fill: 'transparent'
        stroke: c
    el.selectAll '.tick line'
      .attr
        stroke: c
    el.selectAll '.tick text'
      .attr fill: c
    el.append 'text'
      .text 'Myr'
      .attr
        x: s(6)+5
        y: -3

    if labelText
      el.append 'text'
        .text labelText
        .attr
          x: s(0)
          y: -11
          'font-family': 'Helvetica Neue Italic'

    el.selectAll 'text'
      .attr
        fill: c
        'font-size': 7

  F.label = (d)->
    labelText = d
    F

  F
