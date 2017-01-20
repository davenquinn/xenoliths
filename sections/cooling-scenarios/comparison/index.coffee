yaml = require "js-yaml"
d3 = require 'd3'
require 'd3-selection-multi'
fs = require 'fs'
simplify = require 'simplify-js'
xenolithsArea = require 'xenoliths-area'
axes = require 'd3-plot-area/src'

modelColors = require '../shared/colors'
{db, storedProcedure} = require '../shared/database'
util = require '../shared/util'
require './main.styl'
Promise = require 'bluebird'

ax = null
line = null
el = null

dpi = 96
size =
  width: 3.25*dpi
  height: 4.5*dpi

filterX = (data)->
  xd = ax.scale.x.domain()
  data.filter (d)->
    if xd[0] >= d.x or xd[1] <= d.x
      return false
    return true

filterY = (data)->
  yd = ax.scale.y.domain()
  data.filter (d)->
    if yd[1] >= d.y or yd[0] <= d.y
      return false
    return true

makeProfile = (d)->
  util.makeProfile d

setupElement = (rows)->
  for r in rows
    r.profile = filterX filterY(makeProfile(r))

  # Setup labels
  _ = fs.readFileSync __dirname+'/labels.yaml'
  labelData = yaml.load _
  selectedGeotherms = (k for k,v of labelData)

  sel = ax.plotArea().selectAll 'g.model-curve'
    .data rows

  g = sel.enter()
    .append 'g'
    .attrs class: 'model-curve'

  g.append 'defs'
    .append 'path'
      .attrs
        id: (d)-> d.name
        d: (d)->
          line simplify(d.profile,0.005,true)

  g.append 'use'
    .attrs
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
      'stroke-dasharray': (d,i)->
        console.log d
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
      .attrs
        dy: -2
      .append 'textPath'
      .attrs
        'xlink:href': '#'+d.name
        fill: modelColors(d)
        dy: 10
        startOffset: data.offset or '10px'
      .text data.text

  el.selectAll '.tick text'
    .attrs
      'font-size': 8

sql = storedProcedure __dirname+'/get-models.sql'
staticGeotherms = storedProcedure __dirname+'/static-geotherms.sql'

setupStaticGeotherms = (rows)->
  g = ax.plotArea().append 'g'
    .attrs class: 'static-geotherms'

  sel = g.selectAll 'g.static-curve'
    .data rows

  g = sel.enter()
    .append 'g'
    .attrs class: 'static-curve'
  g.append 'defs'
    .append 'path'
      .attrs
        id: (d)-> d.heat_flow
        d: (d)->
          profile = filterX makeProfile(d)
          line simplify(profile,0.005,true)
  g.append 'use'
    .attrs
      'xlink:href': (d)-> '#'+d.heat_flow

  g.each (d,i)->
    d3.select @
      .append 'text'
      .attrs
        dy: 3
      .append 'textPath'
      .attrs
        filter: 'url(#solid)'
        'xlink:href': '#'+d.heat_flow
        startOffset: d.offset or '98%'
      .text d.heat_flow#" mW/m²"

module.exports = (el_, cb)->
  el = d3.select el_
    .append 'svg'
      .attrs size

  el.append 'defs'
    .html fs.readFileSync(__dirname+"/defs.svg")

  ax = axes()
    .neatline()
    .size size
    .margin left: 0.5*dpi, bottom: 0.45*dpi, right: 0.05*dpi, top: 0.1*dpi

  ax.scale.x.domain [800,1200]
  ax.scale.y.domain [90,30]

  ax.axes.y()
    .label "Depth (km)"
    .tickPadding 7
    .tickSize 5
    .ticks 5
    .tickFormat d3.format("i")

  ax.axes.x()
    .label "Temperature (ºC)"
    .tickPadding 7
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

  db.query(staticGeotherms)
    .then setupStaticGeotherms
    .then -> db.query(sql)
    .then setupElement

