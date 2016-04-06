d3 = require 'd3'


fontProperties =
  'font-size': 6
  'font-family': 'Helvetica Neue Light Italic'

module.exports = (ax)->
  loc = (d)->
    {
      x: ax.scale.x(d.time[0])
      y: ax.scale.y(d.lower[0])
    }

  L = (el)->

    g = el.append 'g'
      .attr
        class: 'sub-label'
        transform: (d,i)->
          l = loc(d)
          l.x -= 10 if i != 0
          "translate(#{l.x} #{l.y})"

    g.append 'rect'
      .attr
        width: 22
        height: 8
        y: -10
        x: -1
        fill: 'white'

    g.append 'text'
      .attr
        class: 'oc-age'
        y: -4
      .attr fontProperties
      .text (d)->
        n = d.start_time - d.subduction_time
        "#{n} Myr"

  L.connectingLine = (data)->
    data = data
      .map (d)->[d.time[0],d.lower[0]]
    data.sort()
    v = data[0]
    data.unshift [v[0]-2,v[1]]

    (el)->

      el.append "path"
        .datum data
        .attr
          class: 'label-line'
          d: ax.line()
          stroke: 'black'
          'stroke-width': 0.5
          'stroke-dasharray': '1 0.5'
          fill: 'transparent'
          transform: 'translate(5 -6)'

      v = data[0]
      el.append "text"
        .text "Age of oceanic crust"
        .attr
          x: ax.scale.x v[0]
          y: ax.scale.y v[1]
          dx: 8
          dy: -3.5
        .attr fontProperties

  return L


