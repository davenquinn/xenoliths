_ = require "underscore"
yaml = require "js-yaml"
d3 = require 'd3'
require 'd3-selection-multi'
fs = require 'fs'
legend = require './legend'
layout = require './layout'
G = require './geometry'
{db, storedProcedure} = require '../shared/database'
{makeProfile, lithosphereDepth} = require '../shared/util'
Promise = require 'bluebird'

sql = storedProcedure "#{__dirname}/model-slice.sql"

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync("#{__dirname}/../scenarios.yaml")
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

# Create layouts
wide_layout = layout(5, ["small","large","small","large"])
interval = wide_layout.height()+G.section.spacing.y
offs2 = G.margin.outside + interval

small_layout = -> layout(3, ["small","large"])
sm = small_layout()

forearcOffset = G.margin.outside+sm.width()+G.section.spacing.x
totalWidth = forearcOffset + sm.width()

layouts =
  forearc:
    layout: small_layout()
    position:
      x: forearcOffset
      y: G.margin.outside
  farallon:
    layout: wide_layout
    position:
      x: G.margin.outside
      y: offs2
  underplated:
    layout: small_layout()
    position:
      x: G.margin.outside
      y: G.margin.outside

plotScenarios = (el, scenarios)->
  # Set up scenarios from configuration
  scenarios.forEach (s)->
    s.layout
      .position s.position
      .title s.title
      .labels s.labels

  sel = el.selectAll 'g.scenario'
    .data scenarios
    .enter()
      .append "g"
      .attrs class: 'scenario'

  sel.each (da)->
    d3.select(@).call da.layout
    console.log da.layout.title()
    axes = da.layout.axes()
    axes.forEach (ax,i)=>
      slice = da.slices[i]
      ax.backdrop slice
      ax.labels()
      if i == axes.length-1
        ax.xenolithArea()
      ax.plot slice

  ly = scenarios[2].layout
  g = el.append 'g'
    .attrs
      class: 'legend'
      transform: "translate(#{ly.width()+G.section.spacing.x},#{offs2+ly.topMargin()})"
    .call legend

  el.attrs
    height: offs2 + interval + G.margin.outside
    width: totalWidth

  # Add P-T constraints
  ax = ly.axes()[1]
  g = ax.plotArea().append 'g'

  g.datum {T: 715, z: 25}
  g.attrs
    class: 'constraint'
    transform: (d)->
      "translate(#{ax.scale.x(d.T)},#{ax.scale.y(d.z)})"
  g.append 'circle'
    .attrs
      r: 3
      fill: '#444'
  g.append 'text'
    .text 'Sta. Lucia'
    .attrs
      fill: '#444'
      x: 5
      dy: 4
      'font-size': 8
      'font-family': 'Helvetica Neue'

module.exports = (el_, callback)->
  el = d3.select el_
    .append 'svg'

  scenarios = cfg.map (c)->
    # Integrate layouts
    l = layouts[c.name]
    c.layout = l.layout
    c.position = l.position

    unless c.id.constructor == Array
      c.id = [c.id]
    return c

  getSlices = (s)->
    getSlice = (slice)->
      data = [s.id, slice.id]
      db.query sql,data
        .then (rows)->
          slice.profile = rows.map makeProfile
          slice.rows = rows
          slice.ml = lithosphereDepth(slice.profile)
          return slice
    Promise.map s.slices, getSlice, concurrency:1
      .then (slices)->
        s.slices = slices
        return s

  p = Promise.map scenarios, getSlices, concurrency: 1
    .then (scenarios)-> plotScenarios(el,scenarios)
    .then callback

