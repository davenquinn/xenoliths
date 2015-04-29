d3 = require "d3"
axis = require "./axis"
uuid = require 'node-uuid'
G = require './geometry'

section = 40
large = section/2
small = large/6
edge = small

ticks = small
labels_ = 20
topMargin = 16

axes = null

scale = (layout)->

  (el)->
    pos = layout.position()

    s = pos.y+layout.topMargin()

    el.attr class: "scale"

    yscale = d3.scale.linear()
      .domain [0,90]
      .range [s,s+G.axis.height]

    s = el.append "g"
      .attr class: "scale"

    tl = G.section.horiz.labels

    s.selectAll "line"
      .data [0..9].map (d)->d*10
      .enter()
        .append 'line'
          .attr
            x1: pos.x + tl
            x2: pos.x + layout.width()
            y1: yscale
            y2: yscale
            stroke: "#ccc"
            "stroke-width": 1

    positions = [0,90]
    #text_anchors = ["end","middle","end"]
    #rotation = [0,90,0]
    x = pos.x + G.section.horiz.labels
    dv = "-0.5em"
    anchors = ["0.8em",0]

    s.selectAll "text"
      .data positions
      .enter()
        .append "text"
        .text (d)->d
        .attr
          x: x
          y: yscale
          "text-anchor": "end"
          dy: (d,i)->anchors[i]
          dx: dv

    l = s.append "text"
      .text "km"
      .attr
          transform: "translate(#{x},#{yscale(45)})rotate(-90)"
          "text-anchor": "middle"
          dy: dv

    s.selectAll "text"
      .attr
        "font-family": "Helvetica Neue Light"
        "font-size": 10


module.exports = (n_axes, ax_spacing)->
  ax_spacing = ax_spacing.map (d)->G.axis.spacing.x[d]
  # Axis group
  el = null
  labels = null
  title = null
  position = {x:0,y:0}
  offs = []

  s = G.section
  topMargin = s.title+s.label+s.margin*2
  height = topMargin + G.axis.height

  if not ax_spacing?
    ax_spacing = []
    for i in [1..n_axes-1]
      ax_spacing.push large
  if ax_spacing.length != n_axes-1
    throw "Wrong number of arguments"

  ax_width = G.axis.width

  l = G.section.horiz.labels
  t = G.section.horiz.ticks

  width = l+2*t+ax_width*n_axes+d3.sum ax_spacing

  d = l+t
  offs = [d]
  for s in ax_spacing
    d += s+ax_width
    offs.push d

  createLabels = ->
    return unless labels?
    sel = el.selectAll ".axis-title"
    .data offs

    yoffs = position.y+G.section.title+G.section.margin
    h = G.section.label

    sel.enter()
      .append "text"
      .attr
        class: "axis-title"
        x: (d)->position.x+d
        y: yoffs+h
        "font-size": h
        fill: "#555"
      .text (d,i)->labels[i]

  createTitle = ->
    h = G.section.title
    return unless title?
    el.append "text"
      .text title
      .attr
        class: title
        x: position.x + labels_ + ticks
        y: position.y+h
        "font-size": h

  g = (a)->
    el = a
    el.append "g"
      .call scale(g)

    axes = offs.map (x)->
      pos =
        x: position.x+x
        y: position.y+topMargin
      return axis().position pos

    el.attr
      width: width
      height: height
      x: position.x
      y: position.y

    sel = el.selectAll ".axis"
      .data axes

    sel.enter()
      .append "g"
        .attr
          class: "axis"
          height: G.axis.height
        .each (func)->
          d3.select(@).call func

    createTitle()
    createLabels()

  g.node = -> el
  g.axes = -> axes
  g.title = (o) ->
    return title unless o?
    title = o
    return g

  g.labels = (o) ->
    return labels unless o?
    labels = o
    return g


  g.position = (o)->
    return position unless o?
    position = o
    return g

  g.spacing = (args...)->
    g

  g.topMargin = -> topMargin
  g.width = -> width
  g.height = -> height

  return g
