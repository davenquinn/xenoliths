yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
svgist = require 'svgist'

buildData = require './data'
setupScenarios = require './scenario'

# Create dataset from inputs
dir = fs.readFileSync('/dev/stdin').toString()
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))
data = buildData dir, cfg

# Figure s at 100 ppi
ppi = 100

func = (el)->
  height = 480
  scenarios = setupScenarios data
  d3.select el
    .call scenarios

svgist func, filename: 'build/cooling-scenarios.svg'
