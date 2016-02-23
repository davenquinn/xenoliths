_ = require 'underscore'
savage = require 'savage-svg'
d3 = require 'd3'

query = require '../shared/query'
axis = require '../shared/axis'

sql = "SELECT
  array_agg(t.temperature ORDER BY t.time DESC) AS temperature,
  array_agg(t.time ORDER BY t.time DESC) AS time,
  t.depth AS depth,
  r.name AS run
  FROM thermal_modeling.model_tracer t
  JOIN thermal_modeling.model_run r ON t.run_id = r.id
  GROUP BY t.run_id, r.name, t.depth"

rows = query(sql)

data = rows.map (d)->
  v = _.zip(d.time, d.temperature)
  return {key: d.run, values: v}

func = (el, window)->

  ax = axis()
  ax.scaleX().domain([80,0])
  ax.scaleY().domain([300,1400])

  d3.select(el)
    .attr width: 500, height: 300
    .call ax

  sel = ax.plotArea()
    .selectAll 'path'
    .data data

  path = ax.line()
  sel.enter()
    .append 'path'
    .attr
      stroke: 'grey'
      fill: 'transparent'
      d: (d)->path(d.values)

savage func, filename: 'build/timeline.svg'
