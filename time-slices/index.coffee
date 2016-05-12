yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'savage-svg'
setupScenarios = require './scenario'

# Create dataset from inputs
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))

# Figure s at 100 ppi
ppi = 100

func = (el)->
  scenarios = setupScenarios cfg
  d3.select el
    .call scenarios

savage func, filename: process.argv[2]
