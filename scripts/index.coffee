yaml = require "js-yaml"
jsdom = require 'jsdom'
d3 = require 'd3'
fs = require 'fs'
pd = require 'pretty-data'

buildData = require './data'
setupScenarios = require './scenario'

# Create dataset from inputs
dir = fs.readFileSync('/dev/stdin').toString()
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))
data = buildData dir, cfg

# Figure s at 100 ppi

func = (window)->
  body = window.document.querySelector("body")

  height = 480
  margin = 100
  section_height = (height - 3*margin)/2

  scenarios = setupScenarios data

  global.svg = d3.select body
    .append "svg"
    .attr
      width: 650
      height: height
      xmlns: "http://www.w3.org/2000/svg"
    .call scenarios

  d3.select body
    .html()

jsdom.env
  html: "<html><body></body></html>"
  features:
    QuerySelector: true
  done: (err, window)->
    output = func(window)
    fs.writeFileSync "build/cooling-scenarios.svg", pd.pd.xml(output)

