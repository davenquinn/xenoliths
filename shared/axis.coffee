d3 = require 'd3'

size =
  width: 500
  height: 300
margin = null
innerSize = null

ax = null

x = d3.scale.linear()
y = d3.scale.linear()

line = d3.svg.line()
  .x (d)->x(d[0])
  .y (d)->y(d[1])
  .interpolate 'basis'

__updateInnerSize = ->
  w = size.width-margin.left-margin.right
  h = size.height-margin.top-margin.bottom
  innerSize = {width: w, height: h}
  __updateScaleRanges()

__updateScaleRanges = ->
  x.range([0,innerSize.width])
  y.range([innerSize.height,0])

C = (el)->
  defs = el.append 'defs'

  defs.append 'rect'
    .attr innerSize
    .attr
      id: 'plotArea'
      x: 0
      y: 0
  defs
    .append 'clipPath'
      .attr id: 'plotClip'
      .append 'use'
        .attr 'xlink:href': "#plotArea"

  axContainer = el.append 'g'
    .attr
      transform: "translate(#{margin.left},#{margin.top})"
    .attr innerSize

  ax = axContainer.append 'g'
    .attr 'clip-path': 'url(#plotClip)'

  axContainer.append 'use'
    .attr
      'xlink:href': "#plotArea"
      stroke: 'black'
      fill: 'transparent'

C.plotArea = -> ax
C.line = -> line
C.margin = (d)->
  return margin unless d?
  if d.left?
    margin = d
  else
    margin = {left: d, right: d, top: d, bottom: d}
  __updateInnerSize()

C.scaleX = (s)->
  return x unless s?
  x = s
  __updateScaleRanges()
C.scaleY = (s)->
  return y unless s?
  y = s
  __updateScaleRanges()

C.margin(50)
__updateInnerSize()

module.exports = -> C
