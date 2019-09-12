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
  filterX filterY(util.makeProfile(d, false))

setupElement = (rows)->
  for r in rows
    r.profile = makeProfile(r)

  # Setup labels
  _ = fs.readFileSync __dirname+'/labels.yaml'
  labelData = yaml.load _
  selectedGeotherms = (k for k,v of labelData)

  sel = ax.plotArea().selectAll 'g.model-curve'
    .data rows #.filter (d)->d.index == 0

  g = sel.enter()
    .append 'g'
    .attrs class: (d)->
      cls = 'model-curve'
      cls += util.subductionTypeClasses(d)
      cls

  g.append 'defs'
    .append 'path'
      .attrs
        id: (d)-> d.name
        d: (d)->
          line simplify(d.profile,0.005,true)

  g.append 'use'
    .classed 'selected', (d)->d.index==0
    .attrs
      'xlink:href': (d)-> '#'+d.name
      stroke: (d)->
        c = modelColors(d)
        if d.index != 0
          c = c.alpha(0.5).css()
          #c = c.alpha((1-0.2*d.index)**2.5).css()
        return c
      #'stroke-dasharray': (d,i)->
        #if d.index == 0
          #return 'none'
        #return "#{d.index*0.4+1} #{d.index+1}"
      fill: 'none'

  g.each (d,i)->
    return unless d.name of labelData
    data = labelData[d.name]

    d3.select @
      .append 'text'
      .attrs
        dy: -3
        class: 'run-label'
      .append 'textPath'
      .attrs
        'xlink:href': '#'+d.name
        fill: modelColors(d)
        startOffset: data.offset or '10px'
      .html data.text

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

  e = sel.enter()
    .append 'g'
    .attrs class: 'static-curve'
  e.append 'defs'
    .append 'path'
      .attrs
        id: (d)-> d.heat_flow
        d: (d)->
          profile = filterX makeProfile(d)
          line simplify(profile,0.005,true)
  e.append 'use'
    .attrs
      'xlink:href': (d)-> '#'+d.heat_flow

  e.each (d,i)->
    return if [0,1,11].indexOf(i) != -1
    d3.select @
      .append 'text'
      .attrs
        dy: 3
      .append 'textPath'
      .attrs
        filter: 'url(#solid)'
        'xlink:href': '#'+d.heat_flow
        startOffset: d.offset or '98%'
      .text d.heat_flow

  loc = e.selectAll('text').nodes()[0].getBBox()
  console.log loc

  el.append 'foreignObject'
    .attrs
      class: 'heatflow-label'
      width: 300
      height: 50
      transform: "translate(#{size.width} #{size.height/2}) rotate(90) translate(-150)"
    .append 'xhtml:div'
      .html "Steady-state geotherm with surface heat flow <b>q<sub>0</sub></b> (mW/m<sup>2</sup>)"

module.exports = (el_, opts, cb)->
  el = d3.select el_
    .append 'svg'
      .attrs size

  el.append 'defs'
    .html fs.readFileSync(__dirname+"/defs.svg")

  ax = axes()
    .neatline()
    .size size
    .margin left: 0.5*dpi, bottom: 0.45*dpi, right: 0.1*dpi, top: 0.1*dpi

  ax.scale.x.domain [800,1200]
  ax.scale.y.domain [90,30]

  ax.axes.y()
    .label "Depth (km)"
    .tickPadding 5
    .tickSize 5
    .ticks 5
    .tickFormat d3.format("i")

  ax.axes.x()
    .label "Temperature (°C)"
    .tickPadding 5
    .tickSize 7
    .ticks 5
    .tickFormat d3.format("i")
  el.call ax

  # Suppress last tick label
  #sel = el.select('.axis.x')
    #.selectAll '.tick'
  #sel.filter (d,i)->i == sel.size()-1
    #.select 'text'
      #.text ''

  line = ax.line(type:'object')

  xa = xenolithsArea color: '#ddd', size: 8, showInner: true
  xa ax.plotArea(), ax.line()

  el.select "g:first-child"
    .raise()

  pos = 8
  ypos = ax.scale.y(90)-25
  sz = 20
  ax.plotArea().append 'rect'
    .attrs
      x: pos
      y: ypos
      width: sz
      height: sz
      fill: xa.texture1.url()
      stroke: "#ddd"
      'stroke-width': 1

  textBox = (text, attrs)->(el)->
    fa = ax.plotArea().append "foreignObject"
      .attrs attrs

    fa.append "xhtml:div"
      .text text
      .styles
        'font-size': 9
        'font-family': 'Helvetica Neue'
        'font-style': 'italic'
        'color': '#aaa'


  attrs = {
    x: pos+sz+4
    y: ypos
    width: 80
  }

  ax.plotArea()
    .call textBox("P-T of xenolith entrainment", attrs)

  setupArrows = ->
    x = ax.scale.x(1135)
    y = ax.scale.y(63)
    ax.plotArea().append 'text'
      .text "➞"
      .attrs
        fill: 'limegreen'
        'font-size': 20
        transform: "translate(#{x+8} #{y-8}) rotate(-50)"

    x = ax.scale.x(1135)
    y = ax.scale.y(75)
    ax.plotArea().append 'text'
      .text "➞"
      .attrs
        fill: 'purple'
        'font-size': 20
        transform: "translate(#{x+8} #{y-8}) rotate(-45)"

    ypos -= 20
    x = pos+sz-20
    y = ypos
    ax.plotArea().append 'text'
      .text "➞"
      .attrs
        fill: '#aaa'
        'font-size': 20
        transform: "translate(#{x+8} #{y-8}) rotate(-45)"

    attrs = {
      x: pos+sz+4
      y: ypos-30
      width: 46
    }

    ax.plotArea()
      .call textBox("Direction of model adjustment for erosion", attrs)

  db.query(staticGeotherms)
    .then setupStaticGeotherms
    .then -> db.query(sql)
    .then (data)->
      ix = {}
      for row in data
        ix[row.type] ?= 0
        row.index = ix[row.type]+0
        ix[row.type]+= 1
      data
    .then setupElement
    .tap setupArrows
    .finally cb
