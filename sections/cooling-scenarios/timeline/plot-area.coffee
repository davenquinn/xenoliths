_ = require 'underscore'
d3 = require 'd3'
require 'd3-selection-multi'
textures = require 'textures'

modelColors = require '../shared/colors'

module.exports = (ax)->
  widthOfSubduction = ax.scale.x(0)-ax.scale.x(1.04)

  gen = ax.line().curve d3.curveBasis
  lineUpper = (d)->gen _.zip(d.time, d.upper).reverse()
  lineLower = (d)->gen _.zip(d.time, d.lower)

  (d)->
    upper = lineUpper(d)
    lower = lineLower(d)

    # Create area using SVG path language
    area = upper+'L'+lower.slice(1)+"Z"
    areaID = d.name+'_area'
    clipID = areaID+'_clip'

    el = d3.select @

    defs = el.append 'defs'

    defs.append 'path'
      .datum d
      .attrs
        id: areaID
        fill: modelColors(d).alpha(0.08).css()
        d: area

    el.append 'use'
      .attrs
        href: "#"+areaID
        fill: modelColors(d).alpha(0.08).css()
        d: area

    el.append 'path'
      .datum d
      .attrs
        class: 'tracer'
        stroke: modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: upper
        "stroke-dasharray": '5,1'

    el.append 'path'
      .datum d
      .attrs
        class: 'tracer'
        stroke: modelColors(d).alpha(0.8).css()
        fill: 'transparent'
        d: lower

    if d.subduction_time?
      defs.append 'clipPath'
        .attr 'id', clipID
        .append 'use'
        .attr 'href', '#'+areaID

      tex = textures.lines()
              .orientation('5/8')
              .size 4
              .strokeWidth 0.5
              .stroke modelColors(d).alpha(0.8).css()
      el.call tex

      el.append 'rect'
        .attrs {
          class: 'subduction-area'
          x: ax.scale.x(d.subduction_time)
          width: widthOfSubduction
          y: 0, height: 500
          }
        .attr 'clip-path', "url(##{clipID})"
        .attr 'fill', tex.url()
