yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
simplify = require 'simplify-js'

modelColors = require '../shared/colors'
xenolithsArea = require '../shared/xenoliths-area'
query = require '../shared/query'
util = require '../shared/util'
axes = require '../shared/axes'

sql = "SELECT
    r.*,
    p.name profile_id,
    p.temperature,
    p.dz
  FROM
  thermal_modeling.model_profile p
  JOIN thermal_modeling.model_run r
    ON r.id = p.run_id
  WHERE p.name = 'final'
    AND r.name != 'forearc-28-2'"

staticGeotherms = "SELECT dz, heat_flow, temperature FROM thermal_modeling.static_profile"

selectedGeotherms = ['farallon-reheated-6','underplated-6','forearc-30-10']

rows = query(sql)
#.concat query(staticGeotherms)
console.log rows.length

for r in rows
  r.profile = util.makeProfile r

dpi = 72
size =
  width: 3.25*dpi
  height: 4.5*dpi

func = (el)->
  el = d3.select el
    .attr size

  ax = axes()
    .neatline()
    .size size
    .margin left: 0.5*dpi, bottom: 0.45*dpi, right: 0.05*dpi, top: 0.1*dpi

  ax.scale.x.domain [800,1200]
  ax.scale.y.domain [90,30]

  ax.axes.y()
    .label "Depth (km)"
    .tickOffset 7
    .tickSize 5
    .ticks 5
    .tickFormat d3.format("i")

  ax.axes.x()
    .label "Temperature (ºC)"
    .tickOffset 7
    .tickSize 5
    .ticks 5
    .tickFormat d3.format("i")
  el.call ax

  # Suppress last tick label
  sel = el.select('.axis.x')
    .selectAll '.tick'
  sel.filter (d,i)->i == sel.size()-1
    .select 'text'
      .text ''

  line = ax.line(type:'object')

  xa = xenolithsArea color: '#eee', size: 8
  xa ax.plotArea(), ax.line()

  console.log rows.length
  sel = ax.plotArea().selectAll 'g.data'
    .data rows

  g = sel.enter()
    .append 'g'
    .attr class: 'data'

  g.append 'path'
    .attr
      id: (d)-> d.name
      d: (d)-> line simplify(d.profile,0.005,true)
      stroke: (d)->
        if 'heat_flow' of d
          '#888888'
        else
          modelColors(d).alpha(0.8).css()
      'stroke-width': (d)->
        if d.name in selectedGeotherms
          2
        else
          0.5
      'stroke-dasharray': (d)->
        a = null
        if d.type == 'forearc'
          a = '4 1'
        if d.type == 'underplated'
          a = '2 1'
        a
      fill: 'none'

  g.each (d,i)->
    return if d.name not in selectedGeotherms

    d3.select @
      .append 'text'
      .append 'textPath'
      .attr
        'xlink:href': d.name
        'text-anchor': 'middle'
        startOffset: '90%'
      .text d.name

  el.selectAll '.tick text'
    .attr
      'font-size': 8

savage func, filename: process.argv[2]
