d3 = require "d3"
createBackdrop = require "./backdrop"
plotData = require "./data"
G = require "../geometry"
textures = require '../textures'
uuid = require "uuid"
color = require "color"

module.exports = ->

  container = null
  el = null
  [x,y,w,h] = [0,0,G.axis.width,G.axis.height]
  max = {T: 1700,z: 90}

  axisOutline = (el)->
    el.attr
      x: x
      y: y
      width: w
      height: h

  clipPath = ->
    id = uuid.v1()
    c = (container)->
      container.append "defs"
        .append "svg:clipPath"
          .attr "id", id
          .append "rect"
            .call axisOutline
    c.id = id
    return c

  ax = (container)->
    cp = clipPath()

    container
      .call cp
      .call textures.xenoliths

    el = container.append "g"
      .attr
        class: "inside"
        "clip-path": "url(##{cp.id})"

    container.append "rect"
      .call axisOutline
      .attr
        class: "neatline"
        stroke: "black"
        "stroke-width": 1
        fill: "transparent"

  t = d3.scale.linear()
        .domain [0,max.T]
  d = d3.scale.linear()
        .domain [0,max.z]

  ax.scale =
    temp: t
    depth: d
  ax.line = d3.svg.line()
    .x (d)->ax.scale.temp(d.T)
    .y (d)->ax.scale.depth(d.z)
    .interpolate "basis"

  ax.node = -> el

  ax.width = -> w
  ax.height = -> h
  ax.position = (p)->
    # Takes an object with x and y coordinates
    if p?
      [x,y] = [p.x,p.y]
      ax.scale.depth.range [y,y+h]
      ax.scale.temp.range [x, x+w]
      return ax
    else
      return {x:x,y:y}

  ax.backdrop = createBackdrop ax
  ax.plot = plotData ax
  ax.xenolithArea = ->
    min =
      x: ax.scale.temp 900
      y: ax.scale.depth 40
    max =
      x: ax.scale.temp 1100
      y: ax.scale.depth 80

    ax.node().append "rect"
      .attr min
      .attr
        width: max.x-min.x
        height: max.y-min.y
      .style
        fill: textures.xenoliths.url()

  ax

