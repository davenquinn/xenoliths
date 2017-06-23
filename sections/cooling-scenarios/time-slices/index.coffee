_ = require "underscore"
yaml = require "js-yaml"
d3 = require 'd3'
require 'd3-selection-multi'
fs = require 'fs'
legend = require './legend'
layout = require './layout'
labels = require './labels'
G = require './geometry'
{db, storedProcedure} = require '../shared/database'
{makeProfile, lithosphereDepth, textPath} = require '../shared/util'
Promise = require 'bluebird'
require './main.styl'

sql = storedProcedure "#{__dirname}/model-slice.sql"

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync("#{__dirname}/../scenarios.yaml")
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

# Create layouts
wide_layout = -> layout(5, ["small","large","small","large"])
wl = wide_layout()
interval = wl.height()+G.section.spacing.y
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
    layout: wide_layout()
    position:
      x: G.margin.outside
      y: offs2
  underplated:
    layout: small_layout()
    position:
      x: G.margin.outside
      y: G.margin.outside

alpha = "ABCDEFG"

plotScenarios = (el, scenarios)->
  # Set up scenarios from configuration
  sel = el.selectAll 'div.scenario'
    .data scenarios
    .enter()
      .append "div"
      .attrs class: (d)->"scenario #{d.name}"

  sel.each (da)->
    e = d3.select(@)
    e.append 'h1'
      .html da.title

    label_container = e.append 'div'

    da.svg = e.append 'svg'
    da.svg.call da.layout

    axes = da.layout.axes()
    axes.forEach (ax,i)=>
      slice = da.slices[i]
      ax.backdrop slice
      ax.labels()
      if i == axes.length-1
        ax.xenolithArea()
      ax.plot slice
    label_container.call labels.createAgeLabels(axes, da.slices)

  g = el.append 'div'
    .attrs class: 'legend'
    .call legend

  el.styles width: totalWidth

  ## Apply labels ##
  el.select '.scenario.forearc'
    .call labels.profileLabels
  labels.santaLuciaConstraint(scenarios[2])

  labels.underplatingConstraint(scenarios[0])

module.exports = (el_, callback)->
  el = d3.select el_
    .append 'div'
    .attrs
      id: 'figure'
      width: totalWidth
    .style 'margin','0 0 0 0'

  scenarios = cfg.map (c,i)->
    # Integrate layouts
    l = layouts[c.name]
    c.layout = l.layout
    c.position = l.position

    c.title = "<b>#{alpha[i]}</b>
        <span class='title'>#{c.title}</span>"
    if c.subtitle?
      c.title += " <span class='subtitle'>#{c.subtitle}</span>"

    unless c.id.constructor == Array
      c.id = [c.id]
    return c

  getSlices = (s)->
    getSlice = (slice)->
      data = [s.id, slice.id]
      db.query sql,data
        .then (rows)->
          slice.rows = rows.map (d)->
            d.profile = makeProfile(d)
            return d

          vals = (a)->{z:a.y,T:a.x}
          profiles = slice.rows.map (d)->d.profile.map vals

          # Different depths for mantle lithosphere
          slice.lithosphereDepths = profiles.map lithosphereDepth
          return slice
    Promise.map s.slices, getSlice, concurrency:1
      .then (slices)->
        s.slices = slices
        return s

  p = Promise.map scenarios, getSlices, concurrency: 1
    .then (scenarios)-> plotScenarios(el,scenarios)
    .finally callback

