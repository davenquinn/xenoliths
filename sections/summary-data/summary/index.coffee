fs = require 'fs'
d3 = require 'd3'
require 'd3-selection-multi'
axes = require 'd3-plot-area'
_ = require 'underscore'
require './main.styl'

d = fs.readFileSync "#{__dirname}/temperature-summary.json"
data = JSON.parse d.toString()

dpi = 72
sz = width: dpi*4, height: dpi*3

func = (el, callback)->
  console.log "Started function"
  svg = d3.select el
    .append 'svg'
    .attrs sz

  plot = axes()
    .margin
      left: 0.4*dpi
      bottom: 0.38*dpi
      right: 0.5*dpi
      top: 0.05*dpi
    .size sz

  plot.scale.y
    .domain [920,1120]

  plot.scale.x
    .domain [-0.15,3]

  plot.axes.y(orientation='left')
    .label 'Temperature (°C)'
    .labelOffset 20
    .ticks 5
    .tickSize 3
    .tickFormat d3.format('.0f')

  tnames = ['BKN','Ca-in-Opx','TA98','REE']

  plot.axes.x(orientation='bottom')
    .label 'Thermometer'
    .labelOffset 25
    .tickSize 3
    .tickValues [0..3]
    .tickFormat (d)->tnames[d]


  svg.call plot

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

  g = sel.enter()
    .append 'g'
    .attrs class: 'sample'

  gen = plot.line()
  line = (d,i)->
    ld = d.map (v,i)->[i,v.n]
    gen ld

  agen = (level=1)->
    d3.area()
      .x (d,i)->plot.scale.x i
      .y0 (d)->plot.scale.y d.n-level*d.s
      .y1 (d)->plot.scale.y d.n+level*d.s

  g.append 'path'
    .attrs
      d: agen(2)
      fill: (d)->d.color
      'fill-opacity': 0.05

  g.append 'path'
    .attrs
      d: agen(1)
      fill: (d)->d.color
      'fill-opacity': 0.1

  g.append 'path'
    .attrs
      d: line
      'stroke': (d)->d.color
      'stroke-width': 2
      'fill': 'transparent'

  g.append 'text'
    .text (d)->d.id
    .attrs
      class: (d)->"sample-label #{d.id}"
      y: (d)->
        val = d[d.length-1].n
        plot.scale.y(val)
      x: plot.scale.x(3)

  callback()

module.exports = func
