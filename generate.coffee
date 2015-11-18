global.d3 = require 'd3'
require 'd3-ternary'
fs = require 'fs'
svgist = require 'svgist'

# Get data from Python script
_ = fs.readFileSync('/dev/stdin').toString()
data = JSON.parse(_)

graticule = d3.ternary.graticule()
  .majorInterval 0.2
  .minorInterval 0.05

ternary = d3.ternary.plot()
  .call d3.ternary.scalebars()
  .call d3.ternary.vertexLabels(["Opx","Ol","Cpx"])
  .call d3.ternary.neatline()
  .call graticule


joinData = (el)->
  selection = el
    .selectAll ".dot"
      .data data.features

sz =
  width: 500
  height: 500

createPlot = (el)->

  svg = d3.select el
    .attr sz
    .call ternary
  ternary.fit sz.width,sz.height

  svg.selectAll 'path'
    .attr fill: 'none'

  svg.selectAll 'polygon'
    .attr fill: 'none'

  #ternary.plot().call joinData
svgist createPlot, filename: "output/ternary.svg"
