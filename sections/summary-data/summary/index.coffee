{readFileSync} = require 'fs'
d3 = require 'd3'
conventions = require 'd3-conventions'
require 'd3-selection-multi'
require 'd3-jetpack'
axes = require 'd3-plot-area'
_ = require 'underscore'
require './main.styl'

getJSON = (fn)->
  d = readFileSync require.resolve fn
  JSON.parse d.toString()

data = getJSON "./temperature-summary.json"
depletionData = getJSON "./depletion-summary.json"

console.log depletionData
mergedData = for d in data
  temperature = d.core
  {id, color} = d
  depletion = depletionData.find (v)->v.sample_id == id
  {temperature, depletion, id, color}


dpi = 72
sz = width: dpi*6.5, height: dpi*3

func = (el, callback)->
  console.log mergedData

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

  y = plot.scale.y
    .domain [920,1120]

  #y2 = y.copy()
  #  .domain [0, 40]

  x = plot.scale.x
    .domain [-0.15,6]

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

  sel = plot.plotArea()
    .selectAll 'g.sample'
    .data mergedData

  g = sel.enter()
    .append 'g'
    .attrs class: 'sample'

  tempAtProbability = (level=0)->(d,i)->
    console.log d,i
    t = themometers[i]
    console.log d
    T = d.temperature[t]
    y T.n + level*T.s

  getY = (f)->(d,i)->
    console.log d
    y f(d,i)

  lineData = d3.line()
    .x (d,i)->x(i)
    .y tempAtProbability(0)

  agen = (level=1)->
    d3.area()
      .x (d,i)->x i
      .y0 tempAtProbability(level)
      .y1 tempAtProbability(-level)

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
      d: lineData
      'stroke': (d)->
        console.log d
        d.color
      'stroke-width': 2
      'fill': 'transparent'

  #g.append 'text'
    #.text (d)->d.id
    #.attrs
      #class: (d)->"sample-label #{d.id}"
      #y: (d)->
        #val = d[d.length-1].n
        #plot.scale.y(val)
      #x: plot.scale.x(3)

  callback()

module.exports = func
