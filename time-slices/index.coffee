yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
Scenario = require './scenario'
legend = require './legend'
layout = require './layout'
G = require './geometry'

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

# Create layouts
wide_layout = layout(5, ["small","large","small","large"])
interval = wide_layout.height()+G.section.spacing.y
offs2 = G.margin.outside + interval

small_layout = layout(3, ["small","large"])

forearcOffset = G.margin.outside+small_layout.width()+G.section.spacing.x
totalWidth = forearcOffset + small_layout.width()

layouts =
  forearc:
    layout: small_layout
    position:
      x: forearcOffset
      y: G.margin.outside
  farallon:
    layout: wide_layout
    position:
      x: G.margin.outside
      y: offs2
  underplated:
    layout: small_layout
    position:
      x: G.margin.outside
      y: G.margin.outside

func = (el)->
  el = d3.select el

  cfg.forEach (c)->
    for k,v of layouts[c.name]
      c[k] = v
  console.log cfg

  scenarios = []
  # Set up scenarios from configuration
  sel = el.selectAll 'g.scenario'
    .data cfg
    .enter()
      .append "g"
      .attr class: 'scenario'
      .each (d)->scenarios.push new Scenario(@,d)

  ly = scenarios[2].layout
  g = el.append 'g'
    .attr
      class: 'legend'
      transform: "translate(#{ly.width()+G.section.spacing.x},#{offs2+ly.topMargin()})"
    .call legend

  el.attr
    height: offs2 + interval + G.margin.outside
    width: totalWidth


savage func, filename: process.argv[2]
