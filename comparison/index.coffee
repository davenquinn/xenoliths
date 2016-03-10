yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
simplify = require 'simplify-js'

xenolithsArea = require '../shared/xenoliths-area'
query = require '../shared/query'
util = require '../shared/util'
axis = require '../shared/axis'

sql = "SELECT
    r.name row_id,
    p.name profile_id,
    p.temperature,
    p.dz
  FROM
  thermal_modeling.model_profile p
  JOIN thermal_modeling.model_run r
    ON r.id = p.run_id
  WHERE p.name = 'final'
    AND r.name != 'forearc-28-2'"

staticGeotherms = "SELECT *
  FROM thermal_modeling.static_profile"

rows = query(staticGeotherms)
  .concat query(sql)

for r in rows
  r.profile = util.makeProfile r
  n = r.row_id or r.heat_flow
  console.log n, r.profile[50*100]

dpi = 72
size =
  width: 3.25*dpi
  height: 4.5*dpi

func = (el)->
  el = d3.select el
    .attr size

  ax = axis()
    .size size
    .margin left: 0.5*dpi, bottom: 0.45*dpi, right: 0.05*dpi, top: 0.1*dpi

  ax.scale.x.domain [800,1200]
  ax.scale.y.domain [90,30]

  ax.axes.y()
    .label "Depth (km)"
    .tickOffset 7
    .tickSize 5
    .ticks 10
    .tickFormat d3.format("i")

  ax.axes.x()
    .label "Temperature (ºC)"
    .tickOffset 7
    .tickSize 5
    .ticks 5
    .tickFormat d3.format("i")

  el.call ax

  line = ax.line(type:'object')

  xa = xenolithsArea color: '#ccc', size: 6
  xa ax.plotArea(), ax.line()

  sel = ax.plotArea().selectAll 'path'
    .data rows

  sel.enter()
    .append 'path'
    .attr
      d: (d)-> line simplify(d.profile,0.005,true)
      stroke: (d)->
        if 'heat_flow' of d
          '#888888'
        else
          '#750000'
      fill: 'none'

  el.selectAll 'text'
    .attr
      'font-family': 'Helvetica Neue Light'

savage func, filename: process.argv[2]
