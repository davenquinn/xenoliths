_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'
fs = require 'fs'
path = require 'path'

modelColors = require '../shared/colors'
query = require '../shared/query'
axes = require '../d3-plot-area/src'
plotArea = require './plot-area'
ageLabels = require './age-labels'
legend = require './legend'
underplatingScale = require './underplating-scale'

ff = 'font-family': 'Helvetica Neue Light'

titles = [
  "A. Slab window"
  "B. Stalled slab"
  "C. Late Cretaceous rollback"
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
    top: 0.32*dpi
    bottom: 0.4*dpi
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
    .outerTickSize 0
    .orient 'right'

  el.call ax
  offsY += axsize.height + scaleDelta(spacing)

  plt =  ax.plotArea()
  bkg = plt.append 'g'

  sel = plt
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
  plt.append 'text'
    .text data.title
    .attr
      'font-size': 10
      x: if i == 0 then 3*dpi else 0

  if data.id == 'forearc'
    labels = ageLabels(ax)
    bkg.call labels.connectingLine(data)
    enter.each labels
  if data.id == 'farallon'
    sel
      .filter (d,c)->c==0
      .each ageLabels(ax)


  if data.id != 'forearc'
    k = if data.id == 'farallon' then 80 else 30
    s = underplatingScale(ax)
      .label "Asthenosphere held at #{k} km"
    plt.append('g').call s

  d3.select ax.node()
    .selectAll '.tick text'
    .attr 'font-size': 7

  if i == 1
    plt.append 'text'
      .text 'Monterey Plate'
      .attr
        class: 'annotation'
        fill: modelColors.scales.forearc(30)
        'font-size': 6
        'font-family': 'Helvetica Neue Italic'
        'text-anchor': 'middle'
        transform: (d)->
          x = ax.scale.x(10)
          y = ax.scale.y(1200)
          "translate(#{x},#{y}) rotate(4)"

func = (el, window)->

  g = d3.select(el)
    .attr sz
    .append 'g'

  g.call outerAxes

  g.selectAll '.tick text'
    .attr 'font-size': 8

  plt = outerAxes.plotArea()
  plt.selectAll 'g.axes'
    .data data
    .enter().append 'g'
      .attr class: 'axes'
      .each createAxes

  plt.call legend

savage func, filename: 'build/timeline.svg'
