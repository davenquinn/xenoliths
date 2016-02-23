yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'

buildData = require './data'
setupScenarios = require './scenario'

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

func = (el)->
  height = 480
  scenarios = setupScenarios cfg
  d3.select el
    .call scenarios

savage func, filename: 'build/cooling-scenarios.svg'
