d3 = require 'd3'
require 'd3-selection-multi'

module.exports = (ax)->

  s = d3.scaleLinear()
    .domain [0,6]
    .range [ax.scale.x(24),ax.scale.x(24-6)]

  uScale = d3.axisTop()
    .scale s
    .ticks(4)
    .tickSize -3

  labelText = null

  F = (el)->
    el.attrs
        class: 'u-scale'
        transform: 'translate(0,-5)'
      .call uScale

    c = '#888888'
    el.select '.domain'
      .attrs
        fill: 'transparent'
        stroke: c
    el.selectAll '.tick line'
      .attrs
        stroke: c
    el.selectAll '.tick text'
      .attrs fill: c
    el.append 'text'
      .text 'Myr'
      .attrs
        class: 'myr-label'
        x: s(6)+12
        y: -3

    if labelText
      el.append 'text'
        .text labelText
        .attrs
          x: s(0)
          y: -11

  F.label = (d)->
    labelText = d
    F

  F
