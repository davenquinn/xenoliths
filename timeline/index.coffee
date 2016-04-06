_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'
fs = require 'fs'
path = require 'path'

modelColors = require '../shared/colors'
query = require '../shared/query'
axes = require '../shared/axes'
plotArea = require './plot-area'
ageLabels = require './age-labels'

ff = 'font-family': 'Helvetica Neue Light'

titles = [
  "Slab window"
  "Forearc"
  "Farallon"
]

dpi = 72
names = ['underplated','forearc','farallon']
sz = width: dpi*6.5, height: dpi*4

fn = path.join __dirname,'query.sql'
sql = fs.readFileSync fn

data = (query(sql, [d]) for d in names)
data.forEach (d,i)->
  d.id = names[i]
  d.title = titles[i]
  d.limits = [
    d3.min d, (a)->a.trange[0]
    d3.max d, (a)->a.trange[1]]
  d.axSize = d.limits[1]-d.limits[0]

spacing = 350
spacingBottom = 100
offsY = 0

outerAxes = axes()
  .size sz
  .margin
    right: 0.6*dpi
    left: 0.15*dpi
    top: 0.1*dpi
    bottom: 0.5*dpi
outerAxes.scale.x
  .domain [80,0]

outerAxes.scale.y
  .domain [0, d3.sum(data,(d)->d.axSize)+2*spacing+spacingBottom]
outerAxes.axes.x()
  .label 'Time before present (Ma)'
  .labelOffset 25
  .tickSize 4

vscale = outerAxes.scale.y
scaleDelta = (d)->vscale(0)-vscale(d)

outerAxes.axes.y()
  .label 'Temperature (ºC)'
  .labelOffset 30
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
  # Sort the dataset for predictability
  data.sort (a,b)->a.time[0] < b.time[0]

  el = d3.select @

  axsize =
    width: outerAxes.plotArea.size().width
    height: scaleDelta(data.axSize)

  console.log data.limits,axsize

  ax = axes()
    .size axsize
    .position x: 0, y: offsY
    .margin 0
  ax.scale.x = outerAxes.scale.x
  ax.scale.y.domain data.limits

  ax.axes.y()
    .tickOffset 5
    .tickSize 3
    .ticks Math.floor(data.axSize/200)
    .tickFormat d3.format("i")
    .orient 'right'

  el.call ax
  offsY += axsize.height + scaleDelta(spacing)

  ar =  ax.plotArea()

  bkg = ar.append 'g'

  sel = ar
    .selectAll 'g.model-run'
    .data data

  enter = sel.enter()
    .append 'g'
      .attr class: 'model-run'
      .each plotArea(ax)

  #enter.append 'g'
  #  .attr class: 'profile'
  #  .each createProfileDividers(ax.line())

  # Add title
  ax.plotArea().append 'text'
    .text data.title
    .attr
      'font-size': 10
      dy: 10
      x: if i == 0 then 3*dpi else 0

  if data.id == 'forearc'
    labels = ageLabels(ax)
    bkg.call labels.connectingLine(data)
    enter.each labels
  if data.id == 'farallon'
    sel
      .filter (d,c)->c==0
      .each ageLabels(ax)
    #console.log sel
    #sel.call createAgeLabels(ax)

  d3.select ax.node()
    .selectAll '.tick text'
    .attr 'font-size': 7

func = (el, window)->

  g = d3.select(el)
    .attr sz
    .append 'g'

  g.call outerAxes

  g.selectAll '.tick text'
    .attr 'font-size': 8

  outerAxes.plotArea()
    .selectAll 'g.axes'
    .data data
    .enter().append 'g'
      .attr class: 'axes'
      .each createAxes

savage func, filename: 'build/timeline.svg'
