d3 = require 'd3'
require 'd3-selection-multi'

fontProperties =
  'font-size': 7
  'font-family': 'Helvetica Neue Italic'

module.exports = (ax)->
  loc = (a)->
    {
      x: ax.scale.x(a.time[0])
      y: ax.scale.y(a.lower[0])
    }

  L = (d,i)->
    l = loc(d)
    l.x -= 10 if i != 0
    n = d.start_time - d.subduction_time

    g = d3.select(@)
      .append 'g'
      .attrs
        class: 'sub-label'
        fill: '#888'
        transform: "translate(#{l.x} #{l.y})"

    g.append 'rect'
      .attrs
        width: 26
        height: 8
        y: -10
        x: -2
        fill: 'white'

    g.append 'text'
      .attrs
        class: 'oc-age'
        y: -4
      .attrs fontProperties
      .text "#{n} Myr"

  L.connectingLine = (data)->
    data = data
      .map (d)->[d.time[0],d.lower[0]]
    data.sort()
    v = data[0]
    #data.unshift [v[0]-2,v[1]]

    (el)->

      el.append "path"
        .datum data
        .attrs
          class: 'label-line'
          d: ax.line()
          stroke: '#888'
          'stroke-width': 0.5
          'stroke-dasharray': '1 1'
          fill: 'transparent'
          transform: 'translate(5 -6)'

      _l = {}
      console.log ax.scales
      for k,scale of ax.scale
        n = if k == 'x' then 0 else 1
        val = d3.mean(data,(i)->i[n])
        _l[k] = scale val

      el.append "text"
        .text "Age of initial oceanic lithosphere"
        .attrs
          dy: -10
          transform: "translate(#{_l.x} #{_l.y}) rotate(-7)"
          'text-anchor': 'middle'
          fill: '#888'
        .attrs fontProperties

  return L


