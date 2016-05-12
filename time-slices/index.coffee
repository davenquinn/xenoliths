yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
setupScenarios = require './scenario'
legend = require './legend'

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

func = (el)->
  scenarios = setupScenarios cfg
  el = d3.select el
  el.call scenarios
  g = el.append 'g'
    .attr
      class: 'legend'
      transform: 'translate(300,300)'
  #.call legend

savage func, filename: process.argv[2]
