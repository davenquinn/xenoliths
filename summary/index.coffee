savage = require 'savage-svg'
fs = require 'fs'
d3 = require 'd3'
axes = require 'd3-plot-area'

_ = fs.readFileSync '/dev/stdin'
data = JSON.parse _.toString()

dpi = 72
sz = width: dpi*3.5, height: dpi*3

func = (el, window)->
  svg = d3.select el
    .attr sz

  plot = axes()
    .margin
      left: 0.5*dpi
      bottom: 0.5*dpi
      right: 0.05*dpi
      top: 0.05*dpi
    .size sz

  plot.scale.y
    .domain [900,1100]

  plot.scale.x
    .domain [-0.5,3.5]

  plot.axes.y()
    .label 'Temperature (ºC)'
    .labelOffset 26
    .tickSize 3
    .tickFormat d3.format('.0f')
    .orient 'left'

  svg.call plot

  svg.select '.y text.label'
    .attr 'font-size': 10
  svg.selectAll '.y .tick text'
    .attr 'font-size': 8

savage func, filename: process.argv[2]
