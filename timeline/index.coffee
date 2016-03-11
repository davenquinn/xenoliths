_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'

query = require '../shared/query'
axes = require '../shared/axis'
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

dpi = 72
names = ['underplated','farallon','forearc']
sz = width: dpi*6.5, height: dpi*3.0

data = (query(sql, [d]) for d in names)
limits = data.map (d)->[
  d3.min d, (d)->d.trange[0]
  d3.max d, (d)->d.trange[1]]
axSize = limits.map (d)->d[1]-d[0]

marginTop = 0.05*dpi
offsY = 0

outerAxes = axes()
  .size sz
  .margin
    right: 0
    left: 0
    top: 0.05*dpi
    bottom: 0.05*dpi
outerAxes.scale.x
  .domain [80,0]
outerAxes.scale.y
  .domain [0, d3.sum axSize]

vscale = outerAxes.scale.y

createAxes = (data,i)->
  el = d3.select @

  axsize =
    width: sz.width
    height: vscale(0)-vscale(axSize[i])

  console.log limits[i],axsize

  ax = axes()
    .size axsize
    .position x: 0, y: offsY
    .margin 0
  ax.scale.x = outerAxes.scale.x
  ax.scale.y.domain limits[i]
  el.call ax
  offsY += axsize.height

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
