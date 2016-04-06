_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'
fs = require 'fs'
path = require 'path'

modelColors = require '../shared/colors'
query = require '../shared/query'
axes = require '../shared/axes'
plotArea = require './plot-area'
createAgeLabels = require './age-labels'

ff = 'font-family': 'Helvetica Neue Light'

titles = [
  "Slab window"
  "Farallon"
  "Forearc"
]

dpi = 72
names = ['underplated','farallon','forearc']
sz = width: dpi*6.5, height: dpi*3.0

fn = path.join __dirname,'query.sql'
sql = fs.readFileSync fn

data = (query(sql, [d]) for d in names)
limits = data.map (d)->[
  d3.min d, (d)->d.trange[0]
  d3.max d, (d)->d.trange[1]]
axSize = limits.map (d)->d[1]-d[0]

spacing = 100
offsY = 0

outerAxes = axes()
  .size sz
  .margin
    right: 0.6*dpi
    left: 0.15*dpi
    top: 0.05*dpi
    bottom: 0.5*dpi
outerAxes.scale.x
  .domain [80,0]
outerAxes.scale.y
  .domain [0, d3.sum(axSize)+3*spacing]
outerAxes.axes.x()
  .label 'Time before present (Ma)'

vscale = outerAxes.scale.y
scaleDelta = (d)->vscale(0)-vscale(d)

outerAxes.axes.y()
  .label 'Temperature (ºC)'
  .labelOffset 33
  .despine()
  .orient 'right'

createProfileDividers = (lineGenerator, color)->
  (d)->
    profiles = d.profile.map (a,i)->
      profile: a
      trange: [d.lower[i],d.upper[i]]
      time: d.time[i]

    profiles = profiles.filter (a)->a.profile

    sel = d3.select @
      .selectAll 'path'
      .data profiles

    sel.enter()
      .append 'path'
      .attr
        stroke: modelColors(d).alpha(0.5).css()
        d: (d)->
          console.log d
          t = d.trange.map (a)->[d.time,a]
          lineGenerator(t)

createAxes = (data,i)->

  el = d3.select @

  axsize =
    width: outerAxes.plotArea.size().width
    height: scaleDelta(axSize[i])

  console.log limits[i],axsize

  ax = axes()
    .size axsize
    .position x: 0, y: offsY
    .margin 0
  ax.scale.x = outerAxes.scale.x
  ax.scale.y.domain limits[i]

  ax.axes.y()
    .tickOffset 5
    .tickSize 3
    .ticks Math.floor(axSize[i]/200)
    .tickFormat d3.format("i")
    .orient 'right'

  el.call ax
  offsY += axsize.height + scaleDelta(spacing)

  sel = ax.plotArea()
    .selectAll 'path'
    .data data

  enter = sel.enter()
  enter.call plotArea(ax)

  enter.append 'g'
    .attr class: 'profile'
    .each createProfileDividers(ax.line())

  # Add title
  ax.plotArea().append 'text'
    .text titles[i]
    .attr
      'font-size': 10
      dy: 10
      x: if i == 0 then 3*dpi else 0

  if titles[i] == 'Forearc'
    enter.call createAgeLabels(ax)
  if titles[i] == 'Farallon'
    sel = enter
      .filter (d,c)->c==0
    #console.log sel
    #sel.call createAgeLabels(ax)

#  ax.node().selectAll 'text'
#    .attr ff

func = (el, window)->

  g = d3.select(el)
    .attr sz
    .append 'g'

  g.call outerAxes

  outerAxes.plotArea()
    .selectAll 'g.axes'
    .data data
    .enter().append 'g'
      .attr class: 'axes'
      .each createAxes

savage func, filename: 'build/timeline.svg'
