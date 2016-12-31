savage = require 'savage-svg'
fs = require 'fs'
d3 = require 'd3'
axes = require 'd3-plot-area'
_ = require 'underscore'

d = fs.readFileSync '/dev/stdin'
data = JSON.parse d.toString()

dpi = 72
sz = width: dpi*3.5, height: dpi*3

func = (el, window)->
  svg = d3.select el
    .attr sz

  plot = axes()
    .margin
      left: 0.5*dpi
      bottom: 0.35*dpi
      right: 0.15*dpi
      top: 0.05*dpi
    .size sz

  plot.scale.y
    .domain [920,1120]

  plot.scale.x
    .domain [-0.15,3]

  plot.axes.y()
    .label 'Temperature (ºC)'
    .labelOffset 26
    .tickSize 3
    .tickFormat d3.format('.0f')
    .orient 'left'

  tnames = ['BKN','Ca-in-Opx','TA98','REE']

  plot.axes.x()
    .label 'Thermometer'
    .tickSize 3
    .tickValues [0..3]
    .tickFormat (d)->tnames[d]

  svg.call plot

  svg.select '.y text.label'
    .attr 'font-size': 10
  svg.selectAll '.y .tick text'
    .attr 'font-size': 8

  svg.selectAll '.x .tick text'
    .attr
      'font-size': 9
      color: '#666'

  thermometers = ['bkn','ca_opx_corr','ta98','ree']
  data = data.map (s)->
    console.log s
    d = thermometers.map (t)->s.core[t]
    d.id = s.id
    d.color = s.color
    return d

  sel = plot.plotArea()
    .selectAll 'g.sample'
    .data data

  group = sel.enter()
    .append 'g'
    .attr class: 'sample'

  gen = plot.line()
  line = (d,i)->
    ld = d.map (v,i)->[i,v.n]
    gen ld

  agen = (level=1)->
    d3.svg.area()
      .x (d,i)->plot.scale.x i
      .y0 (d)->plot.scale.y d.n-level*d.s
      .y1 (d)->plot.scale.y d.n+level*d.s

  sel.append 'path'
    .attr
      d: agen(2)
      fill: (d)->d.color
      'fill-opacity': 0.05

  sel.append 'path'
    .attr
      d: agen(1)
      fill: (d)->d.color
      'fill-opacity': 0.1

  sel.append 'path'
    .attr
      d: line
      'stroke': (d)->d.color
      'stroke-width': 2
      'fill': 'transparent'

savage func, filename: process.argv[2]
