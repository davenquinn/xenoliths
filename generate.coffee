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
  .call d3.ternary.vertexLabels(["Ol","Opx","Cpx"])
  .call d3.ternary.neatline()
  .call graticule

joinData = (el)->
  selection = el
    .selectAll ".dot"
      .data data.features

sz =
  width: 500
  height: 500

sets =
  Quinn:
    r: 4
    fill: (d)->d.color
  Luffi:
    r: 3
    fill: '#888'
  other:
    r: 3
    fill: '#aaa'

createPlot = (el)->

  svg = d3.select el
    .attr sz
    .call ternary
  ternary.fit sz.width,sz.height

  svg.selectAll 'path'
    .attr fill: 'none'

  svg.select '.neatline'
    .attr
      fill: 'none'
      stroke: 'black'

  svg.selectAll '.graticule path'
    .attr
      stroke: '#aaaaaa'
      'stroke-width': ->
        maj = d3.select @
          .classed 'major'
        if maj then 1 else 0.5

  ternary.plot()
    .selectAll 'circle'
    .data(data)
    .enter()
      .append 'circle'
      .attr
        class: (d)->"data #{d.source}"
        r: 2
      .each (d)->
        v = [d.ol,d.cpx,d.opx]
        c = ternary.point v

        d3.select @
          .attr sets[d.source] or sets.other
          .attr
            cx: c[0]
            cy: c[1]

  #ternary.plot().call joinData
svgist createPlot, filename: "output/ternary.svg"
