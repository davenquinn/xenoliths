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
    n = d.start_time - d.subduction_time

    g = d3.select(@)
      .append 'g'
      .attrs
        class: 'sub-label'
        fill: '#888'
        transform: "translate(#{l.x} #{l.y+2})"

    g.append 'text'
      .attrs
        class: 'oc-age'
        x: -3
        'text-anchor': 'end'
      .html "<tspan>#{n} Myr</tspan><tspan x=-3 dy=7 class='smaller'>#{d.start_time} Ma</tspan>"

  L.axisLabel = (x,y)->(el)->
    el.append "text"
      .html "
        <tspan>Age of initial oceanic lithosphere</tspan>
        <tspan x=0 dy=7 class='smaller'>Timing of spreading-ridge emplacement</tspan>"
      .attrs
        class: 'oc-age-label'
        dy: -10
        transform: "translate(#{x} #{y})"
        'text-anchor': 'start'
        fill: '#888'

  return L


