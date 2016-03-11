_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'

query = require '../shared/query'
axes = require '../shared/axes'
modelColors = require '../shared/colors'

subquery1 = "SELECT
  min(t.temperature) AS min_temp,
  max(t.temperature) AS max_temp,
  array_agg(t.temperature ORDER BY t.time DESC) AS temperature,
  array_agg(t.time ORDER BY t.time DESC) AS time,
  t.final_depth AS depth,
  t.run_id AS id
  FROM thermal_modeling.model_tracer t
  JOIN thermal_modeling.model_run r ON t.run_id = r.id
  WHERE r.type LIKE $1::text || '%'
    AND r.name != 'forearc-28-2'
  GROUP BY t.run_id, r.name, t.final_depth"

sql = "WITH a AS (#{subquery1}),
  u AS (SELECT * FROM a WHERE a.depth = 40),
  l AS (SELECT * FROM a WHERE a.depth = 80)
  SELECT
    r.*,
    u.time,
    array[u.min_temp,l.max_temp] trange,
    u.temperature upper,
    l.temperature lower
  FROM u
  JOIN l ON u.id = l.id
  JOIN thermal_modeling.model_run r ON u.id = r.id"

titles = [
  "Slab window"
  "Farallon"
  "Forearc"
]

dpi = 72
names = ['underplated','farallon','forearc']
sz = width: dpi*6.5, height: dpi*3.0

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
    bottom: 0.3*dpi
outerAxes.scale.x
  .domain [80,0]
outerAxes.scale.y
  .domain [0, d3.sum(axSize)+3*spacing]
outerAxes.axes.x()
  .label('Model time (Ma)')

vscale = outerAxes.scale.y
scaleDelta = (d)->vscale(0)-vscale(d)

outerAxes.axes.y()
  .label 'Temperature (ºC)'
  .labelOffset 33
  .despine()
  .orient 'right'

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

  gen = ax.line().interpolate('basis')
  line = (key)->
    (d)-> gen _.zip(d.time, d[key])

  agen = d3.svg.area()
    .x (d)->ax.scale.x d[0]
    .y0 (d)->ax.scale.y d[1]
    .y1 (d)->ax.scale.y d[2]
  area = (d)->
    agen _.zip(d.time, d['lower'], d['upper'])

  sel = ax.plotArea()
    .selectAll 'path'
    .data data

  enter = sel.enter()

  enter.append 'path'
    .attr
      fill: (d)->modelColors(d).alpha(0.2).css()
      d: area

  enter.append 'path'
    .attr
      class: 'tracer'
      stroke: (d)->modelColors(d).alpha(0.8).css()
      fill: 'transparent'
      d: line('upper')
      "stroke-dasharray": '5,1'

  enter.append 'path'
    .attr
      class: 'tracer'
      stroke: (d)->modelColors(d).alpha(0.8).css()
      fill: 'transparent'
      d: line('lower')

  # Add title
  ax.plotArea().append 'text'
    .text titles[i]
    .attr
      'font-size': 10
      dy: 10
      x: if i == 0 then 3*dpi else 0

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
