yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
savage = require 'svg-shim'

buildData = require './data'
setupScenarios = require './scenario'

# Create dataset from inputs
dir = fs.readFileSync('/dev/stdin').toString()
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))
data = buildData dir, cfg

# Figure s at 100 ppi

func = (el)->
  height = 480
  margin = 100
  section_height = (height - 3*margin)/2

  scenarios = setupScenarios data

  d3.select el
    .append "svg"
    .attr
      width: 650
      height: height
      xmlns: "http://www.w3.org/2000/svg"
    .call scenarios

savage func, filename: 'build/cooling-scenarios.svg'
