fs = require 'fs'
d3 = require 'd3'
require 'd3-selection-multi'
xenolithsArea = require 'xenoliths-area'
require './main.styl'

module.exports = (el_,cb)->
  el_.innerHTML = fs.readFileSync("ca-ol-pressures.svg")

  el = d3.select "svg"

  plotArea = d3.select "#patch_2"

  bbox = plotArea.node().getBBox()

  x = d3.scaleLinear()
        .range([bbox.x,bbox.x+bbox.width])
        .domain([900,1150])
  y = d3.scaleLinear()
        .range([bbox.y+bbox.height,bbox.y])
        .domain([90,10])

  line = d3.line()
    .x (d)->x(d[0])
    .y (d)->y(d[1])

  xa = xenolithsArea(color: "#eee")
  xa plotArea, line

  pos = 145
  ypos = y(12)
  sz = 17
  plotArea.append 'rect'
    .attrs
      x: pos
      y: ypos
      width: sz
      height: sz
      fill: xa.texture.url()
      stroke: "#fbfbfb"
      'stroke-width': 0.5

  fa = plotArea.append "foreignObject"
    .attrs
      x: pos+sz+2
      y: ypos
      width: 50

  fa.append "xhtml:div"
    .text "Probable P-T constraints"
    .styles
      'font-size': 7
      'font-family': 'Helvetica Neue'
      'font-style': 'italic'
      'color': '#ccc'

  cb()
