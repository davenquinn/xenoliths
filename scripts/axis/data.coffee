d3 = require "d3"
simplifiedLine = require '../simplified-line'

module.exports = (ax)->

  el = null
  out = (data)->
    el = ax.node()
    el.append "path"
      .datum [0,90].map (d)->
        {z:d, T:1300}
      .attr
        d: ax.line
        "stroke-width": 1
        "stroke-dasharray": "2,2"
        stroke: "#666666"


    x = ax.scale.temp 1300
    y = ax.scale.depth 90
    t = "translate(#{x},#{y})rotate(-90)"
    label = el.append "text"
      .text "1300º C"
      .attr
        transform: t
        "font-family": "Gotham Book"
        "font-size": 8
        fill: "#666666"
        dy: -3
        dx: 2

    lowTempBase = ->
      for d in data.profile[0] by 10
        if d.z >= 90
          return d.T < 1300

    if lowTempBase()
      label.attr dy: 8

    sel = el.selectAll "path.data"
      .data data.profile.filter (d)->d?

    sel.enter()
      .append "path"
      .attr
        class: "data"
        id: (d,i)->data.id[i]
        d: simplifiedLine ax.scale, 0.005
        "stroke-width": 2
        stroke: '#750000'
        fill: "transparent"

  return out
