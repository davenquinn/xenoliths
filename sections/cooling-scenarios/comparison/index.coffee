yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
simplify = require 'simplify-js'
xenolithsArea = require 'xenoliths-area'

modelColors = require '../shared/colors'
{db, storedProcedure} = require '../shared/database'
util = require '../shared/util'
axes = require '../d3-plot-area/src'

staticGeotherms = "SELECT dz, heat_flow, temperature FROM thermal_modeling.static_profile"

module.exports = (el, callback)->

  sql = storedProcedure __dirname+'/query.sql'
  rows = db.query(sql)
  #.concat query(staticGeotherms)
  console.log rows.length

  for r in rows
    r.profile = util.makeProfile r

  dpi = 72
  size =
    width: 3.25*dpi
    height: 4.5*dpi

  # Setup labels
  _ = fs.readFileSync __dirname+'/labels.yaml'
  labelData = yaml.load _
  selectedGeotherms = (k for k,v of labelData)

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

  g.append 'defs'
    .append 'path'
      .attr
        id: (d)-> d.name
        d: (d)-> line simplify(d.profile,0.005,true)

  g.append 'use'
    .attr
      'xlink:href': (d)-> '#'+d.name
      stroke: (d)->
        if 'heat_flow' of d
          '#888888'
        else
          c = modelColors(d)
          if d.name in selectedGeotherms
            return c.alpha(0.8).css()
          else
            return c.alpha(0.2).css()
      'stroke-width': (d)->
        if d.name in selectedGeotherms
          2
        else
          1
      'stroke-dasharray': (d)->
        a = null
        if d.type == 'forearc'
          a = '4 1'
        if d.type == 'underplated'
          a = '2 1'
        a
      fill: 'none'

  g.each (d,i)->
    return unless d.name of labelData

    data = labelData[d.name]

    d3.select @
      .append 'text'
      .attr
        'font-family': 'Helvetica Neue'
      .append 'textPath'
      .attr
        'xlink:href': '#'+d.name
        fill: modelColors(d)
        'font-size': 10
        startOffset: data.offset or '50%'
        dy: -2
      .text data.text.replace(' ','_')

  el.selectAll '.tick text'
    .attr
      'font-size': 8

  callback()

