uuid = require 'uuid'
d3 = require 'd3'

defaults =
  neatline: true

styleAxis = (g)->
  g.selectAll 'path.domain'
    .attr fill: 'none', stroke: 'black'
  g.selectAll '.tick line'
    .attr stroke: '#000000'

xaxis = (ax)->
  g = null
  label = null
  tickOffset = 10
  labelSize = 10
  labelOffset = 22

  _y = d3.svg.axis()

  y = ->
    g = d3.select(@)
      .append("g")
        .attr class: "x axis"

    g.append "text"
      .attr
        class: 'label'
      .style 'text-anchor': "middle"
      .text label
    g.call _y
    g.call styleAxis
    y.update()

  y.update = ->
    sz = ax.plotArea.size()

    g.attr
      transform: "translate(0,#{sz.height})"

    g.select 'text.label'
      .attr
        transform: "translate(#{sz.width/2},0)"
        'font-size': labelSize
        dy: labelOffset

    g.selectAll ".tick text"
      .attr
        'text-anchor':"middle"
        "font-size": 10

    if ax.grid()
      g.selectAll '.tick .grid'
        .attr x1: sz.height

  y.tickOffset = (d)->
    return tickOffset unless d?
    tickOffset = d
    return y

  y.label = (d)->
    return label unless d?
    label = d
    return y

  y.labelOffset = (d)->
    return labelOffset unless d?
    labelOffset = d
    return y

  for k,v of _y
    y[k] = v

  y.scale ax.scale.x
  y.orient "bottom"

  return y

yaxis = (ax)->
  g = null
  label = null
  labelSize = 10
  labelOffset = 20
  tickOffset = 10
  _despined = false

  _y = d3.svg.axis()

  y = ->
    g = d3.select(@)
      .append("g")
        .attr class: "y axis"

    g.append "text"
      .attr
        class: 'label'
        dy: -labelOffset
      .style 'text-anchor': "middle"
      .text label
    if not _despined
      g
        .call _y
        .call styleAxis

    y.update()

  y.update = ->
    sz = ax.plotArea.size()
    right = y.orient() == 'right'
    rot = 90
    rot *= -1 if not right

    g.select 'text.label'
      .attr
        transform: "translate(0,#{sz.height/2})rotate(#{rot})"
        'font-size': labelSize

    g.selectAll ".tick text"
      .attr
        'text-anchor':"middle"
        "font-size": 10

    if ax.grid()
      g.selectAll '.tick .grid'
        .attr x1: sz.width

    if right
      g.attr transform: "translate(#{sz.width},0)"

  y.tickOffset = (d)->
    return tickOffset unless d?
    tickOffset = d
    return y

  y.label = (d)->
    return label unless d?
    label = d
    return y

  y.labelOffset = (d)->
    return labelOffset unless d?
    labelOffset = d
    return y

  y.despine = ->
    _despined = true
    return y

  for k,v of _y
    y[k] = v

  y.scale ax.scale.y
  y.orient "left"

  return y

module.exports = (opts={})->
  for k,o of defaults
    continue if k of opts
    opts[k] = o

  C = null
  size =
    width: 500
    height: 300
  offset =
    x: 0
    y: 0
  axTrans = null
  margin = 0
  innerSize = null

  _grid = true
  _neatline = false
  _clip = false
  node = null
  ax = null
  neatline = null
  graticule = null
  _xax = null
  _yax = null

  x = d3.scale.linear()
  y = d3.scale.linear()
  scales  = {x: x, y: y}

  line = (opts={})->

    l = d3.svg.line()

    type = opts.type or 'array'
    if type == 'array'
      l.x (d)->C.scale.x(d[0])
      l.y (d)->C.scale.y(d[1])
    else if type == 'object'
      l.x (d)->C.scale.x(d.x)
      l.y (d)->C.scale.y(d.y)

    if opts.interpolate?
      l.interpolate opts.interpolate
    return l

  __update = ->
    # Inner size
    w = size.width-margin.left-margin.right
    h = size.height-margin.top-margin.bottom
    innerSize = {width: w, height: h}

    axTrans =
      x: offset.x + margin.left
      y: offset.y + margin.top

    # Scale ranges
    C.scale.x.range([0,innerSize.width])
    C.scale.y.range([innerSize.height,0])

    _xax.update() if _xax?
    _yax.update() if _yax?

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

    #t1 = "translate(#{offset.x},#{offset.y})"

    axContainer = el .append 'g'
      .attr
        transform: " translate(#{axTrans.x},#{axTrans.y})"
      .attr innerSize

    graticule = axContainer.append 'g'

    ax = axContainer.append 'g'

    if _clip
      ax.attr 'clip-path': "url(##{clipID})"

    if _neatline
      neatline = axContainer.append 'use'
        .attr
          'xlink:href': "#"+areaID
          class: 'neatline'
          stroke: 'black'
          fill: 'transparent'

    if _xax?
      _xax.call graticule.node()
    if _yax?
      _yax.call graticule.node()

  C.axes =
    x: ->
      if not _xax?
        _xax = xaxis C
      _xax
    y: ->
      if not _yax?
        _yax = yaxis C
      _yax

  C.grid = (g)->
    if g?
      _grid = g
      return C
    else
      return _grid

  C.node = -> node
  C.plotArea = -> ax
  C.plotArea.size = -> innerSize
  C.neatline = (v)->
    v = true unless v?
    _neatline = v
    _clip = v
    return C
  C.clip = (v)->
    v = true unless v?
    _clip = v
    return C
  C.graticule = -> graticule
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
    __update()
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

  C.position = (p)->
      # Takes an object with x and y coordinates
    return offset unless p?
    for k,v of offset
      offset[k] = p[k] if k of p
    __update()
    return C

  C.reflow = __update

  C.margin(50)
  __update()

  return C
