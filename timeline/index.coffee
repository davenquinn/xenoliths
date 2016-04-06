_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'

query = require '../shared/query'
axes = require '../shared/axes'
modelColors = require '../shared/colors'

ff = 'font-family': 'Helvetica Neue Light'

subquery1 = "SELECT
  array_agg(p.time ORDER BY p.time DESC) AS profile_time,
  p.run_id AS id
  FROM thermal_modeling.model_profile p
  JOIN thermal_modeling.model_run r ON p.run_id = r.id
  GROUP BY p.run_id"

subquery2 = "SELECT
  min(t.temperature) AS min_temp,
  max(t.temperature) AS max_temp,
  array_agg(t.temperature ORDER BY t.time DESC) AS temperature,
  array_agg(t.time ORDER BY t.time DESC) AS time,
  array_agg(t.time = ANY(a.profile_time) ORDER BY t.time DESC) AS profile_time,
  t.final_depth AS depth,
  t.run_id AS id
  FROM thermal_modeling.model_tracer t
  JOIN thermal_modeling.model_run r ON t.run_id = r.id
  JOIN a ON a.id = r.id
  WHERE r.type LIKE $1::text || '%'
    AND r.name != 'forearc-28-2'
  GROUP BY t.run_id, r.name, t.final_depth, a.profile_time"

sql = "WITH
  a AS (#{subquery1}),
  b AS (#{subquery2}),
  u AS (SELECT * FROM b WHERE b.depth = 40),
  l AS (SELECT * FROM b WHERE b.depth = 75)
  SELECT
    r.*,
    u.time,
    u.profile_time profile,
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

console.log sql

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
  .label('Time before present (Ma)')

vscale = outerAxes.scale.y
scaleDelta = (d)->vscale(0)-vscale(d)

outerAxes.axes.y()
  .label 'Temperature (ºC)'
  .labelOffset 33
  .despine()
  .orient 'right'

createAgeLabels = (ax)->
  (el)->
    el.append 'text'
      .attr
        class: 'oc-age'
        x: (d)->ax.scale.x(d.time[0])
        y: (d)->ax.scale.y(d.lower[0])
        dy: -2
        dx: -10
        'font-size': 6
        'font-family': 'Helvetica Neue Light Italic'
      .text (d)->
        n = d.start_time - d.subduction_time
        "#{n} Myr"


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

  enter.append 'g'
    .attr class: 'profile'
    .each createProfileDividers(gen)

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
    console.log sel
    sel.call createAgeLabels(ax)

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
