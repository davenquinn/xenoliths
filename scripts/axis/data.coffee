d3 = require "d3"
simplify = require "simplify-js"

module.exports = (ax)->

  simplifiedLine = (amount=1)->
    line = d3.svg.line()
      .x (d)->d.x
      .y (d)->d.y

    (data)->
      d = data.map (d)->
        {
          x: ax.scale.temp d.T
          y: ax.scale.depth d.z
        }
      l = simplify d,amount,true
      line l

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
      .data data.profile

    sel.enter()
      .append "path"
      .attr
        class: "data"
        id: (d,i)->data.id[i]
        d: simplifiedLine 0.005
        "stroke-opacity": (d,i)->
          if i == 0 then 1 else 0.5
        "stroke-width": 2
        stroke: '#750000'
        fill: "transparent"

  return out
