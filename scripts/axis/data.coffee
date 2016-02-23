d3 = require "d3"
simplify = require 'simplify-js'

ax = null
el = null

module.exports = (ax)->
  out = (data)->
    line = ax.line(type:'object')

    el = d3.select ax.node()
    el.append "path"
      .datum [0,90].map (d)->
        {x:1300,y:d}
      .attr
        d: line
        "stroke-width": 1
        "stroke-dasharray": "2,2"
        stroke: "#666666"

    x = ax.scale.x 1300
    y = ax.scale.y 90
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
        if d.y >= 90
          return d.x < 1300

    if lowTempBase()
      label.attr dy: 8

    sel = el.selectAll "path.data"
      .data data.profile.filter (d)->d?

    sel.enter()
      .append "path"
      .attr
        class: "data"
        id: (d,i)->data.id[i]
        d: (d)->line simplify(data,0.005,true)
        "stroke-width": 2
        stroke: '#750000'
        fill: "transparent"

  return out
