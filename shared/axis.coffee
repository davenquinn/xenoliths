uuid = require 'uuid'
d3 = require 'd3'

size =
  width: 500
  height: 300
offset =
  x: 0
  y: 0
margin = null
innerSize = null

node = null
ax = null
neatline = null

x = d3.scale.linear()
y = d3.scale.linear()
scales  = {x: x, y: y}

line = (opts={})->

  l = d3.svg.line()

  type = opts.type or 'array'
  if type == 'array'
    l.x (d)->x(d[0])
    l.y (d)->y(d[1])
  else if type == 'object'
    l.x (d)->x(d.x)
    l.y (d)->x(d.y)

  if opts.interpolate?
    l.interpolate opts.interpolate
  return l

__update = ->
  # Inner size
  w = size.width-margin.left-margin.right
  h = size.height-margin.top-margin.bottom
  innerSize = {width: w, height: h}

  # Scale ranges
  scales.x.range([0,innerSize.width])
  scales.y.range([innerSize.height,0])

C = (el)->
  node = el.node()
  defs = el.append 'defs'

  areaID = uuid.v1()
  clipID = uuid.v1()

  defs.append 'rect'
    .attr innerSize
    .attr
      id: areaID
      x: 0
      y: 0
  defs
    .append 'clipPath'
      .attr id: clipID
      .append 'use'
        .attr 'xlink:href': "#"+areaID

  console.log C.boundingBox(), innerSize, margin

  t1 = "translate(#{offset.x},#{offset.y})"

  axContainer = el.append 'g'
    .attr
      transform: t1+" translate(#{margin.left},#{margin.top})"
    .attr innerSize

  ax = axContainer.append 'g'
    .attr 'clip-path': "url(##{clipID})"

  neatline = axContainer.append 'use'
    .attr
      'xlink:href': "#"+areaID
      class: 'neatline'
      stroke: 'black'
      fill: 'transparent'

C.node = -> node
C.plotArea = -> ax
C.neatline = -> neatline
C.line = line
C.boundingBox = ->
    left: offset.x,
    top: offset.y,
    bottom: offset.y + size.height
    right: offset.x + size.width

C.size = (d)->
  # Getter/setter for plot size
  return size unless d?
  for k,v of size
    size[k] = d[k] if k of d
  return C

C.margin = (d)->
  return margin unless d?
  if d.left?
    margin = d
  else
    margin = {left: d, right: d, top: d, bottom: d}
  __update()
  return C

C.scale = scales

C.scaleX = (s)->
  return x unless s?
  x = s
  __update()
C.scaleY = (s)->
  return y unless s?
  y = s
  __update()
C.position = (p)->
    # Takes an object with x and y coordinates
  return offset unless p?
  for k,v of offset
    offset[k] = p[k] if k of p
  __update()
  return C
C.margin(50)
C.reflow = __update

__update()

module.exports = -> C
