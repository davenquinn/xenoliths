yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
simplify = require 'simplify-js'

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

rows = query(sql)
for r in rows
  r.profile = util.makeProfile r

dpi = 72
size =
  width: 3.25*dpi
  height: 4.5*dpi

func = (el)->
  el = d3.select el
    .attr size

  ax = axis()
    .size size
    .margin 0.25*dpi

  ax.scale.x.domain [800,1300]
  ax.scale.y.domain [90,30]

  el.call ax

  line = ax.line(type:'object')

  sel = ax.plotArea().selectAll 'path'
    .data rows

  sel.enter()
    .append 'path'
    .attr
      d: (d)-> line simplify(d.profile,0.005,true)
      stroke: '#750000'
      fill: 'none'

savage func, filename: process.argv[2]
