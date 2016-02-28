_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'

query = require '../shared/query'
axis = require '../shared/axis'

subquery1 = "SELECT
  min(t.temperature) AS min_temp,
  max(t.temperature) AS max_temp,
  array_agg(t.temperature ORDER BY t.time DESC) AS temperature,
  array_agg(t.time ORDER BY t.time DESC) AS time,
  t.final_depth AS depth,
  r.name AS run
  FROM thermal_modeling.model_tracer t
  JOIN thermal_modeling.model_run r ON t.run_id = r.id
  WHERE r.name LIKE $1::text || '%'
    AND r.name != 'forearc-28-2'
  GROUP BY t.run_id, r.name, t.final_depth"

sql = "WITH a AS (#{subquery1}),
  u AS (SELECT * FROM a WHERE a.depth = 40),
  l AS (SELECT * FROM a WHERE a.depth = 80)
  SELECT
    u.run,
    u.time,
    array[u.min_temp,l.max_temp] trange,
    u.temperature upper,
    l.temperature lower
  FROM u JOIN l ON u.run = l.run
  "

dpi = 72
names = ['farallon','underplated','forearc']
sz = width: dpi*6.5, height: dpi*3.5

data = (query(sql, [d]) for d in names)
limits = data.map (d)->[
  d3.min d, (d)->d.trange[0]
  d3.max d, (d)->d.trange[1]]
axLims = limits.map (d)->[
  Math.floor(d[0]/100)*100,
  Math.ceil(d[1]/100)*100]
axSize = axLims.map (d)->d[1]-d[0]

console.log axLims

vscale = d3.scale.linear()
  .domain [0, d3.sum axSize]
  .range [0,sz.height]

offsY = 0
createAxis = (data,i)->
  el = d3.select @

  axsize =
    width: sz.width
    height: vscale(axSize[i])

  ax = axis neatline: false, clip: false
    .size axsize
    .position x: 0, y: offsY
    .margin 0
  ax.scale.x.domain([80,0])
  ax.scale.y.domain axLims[i]
  el.call ax
  offsY += axsize.height

  gen = ax.line()
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
      fill: 'rgba(100,100,100,0.2)'
      d: area

  enter.append 'path'
    .attr
      stroke: 'grey'
      fill: 'transparent'
      d: line('upper')
      "stroke-dasharray": '5,1'

  enter.append 'path'
    .attr
      stroke: 'grey'
      fill: 'transparent'
      d: line('lower')

func = (el, window)->

  sel = d3.select(el)
    .attr sz

  sel.selectAll 'g.axis'
    .data data
    .enter().append 'g'
      .attr class: 'axis'
      .each createAxis

savage func, filename: 'build/timeline.svg'
