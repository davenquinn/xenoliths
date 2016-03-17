global.d3 = require 'd3'
require './d3-ternary/src/ternary'
fs = require 'fs'
savage = require 'savage-svg'

# Get data from Python script
_ = fs.readFileSync('/dev/stdin').toString()
data = JSON.parse(_)

graticule = d3.ternary.graticule()
  .majorInterval 0.1
  .minorInterval 0.05

scalebar = d3.ternary.scalebars()
  .labels ["Olivine","",""]
scalebar.axes[0].tickValues (i/10 for i in [5..9])
scalebar.axes[1].tickValues []
scalebar.axes[2].tickValues []


ternary = d3.ternary.plot()
  .clip(true)
  .call scalebar
  .call d3.ternary.vertexLabels(["Ol",'Opx₅₅','Cpx₅₅'])
  .call d3.ternary.neatline()
  .call graticule

ternary.scales[0].domain [0.4,1]
ternary.scales[1].domain [0,0.6]
ternary.scales[2].domain [0.6,0]

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
      stroke: '#cccccc'
      'stroke-width': ->
        maj = d3.select @
          .classed 'major'
        if maj then 0.5 else 0.25

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

savage createPlot, filename: "output/ternary.svg"
