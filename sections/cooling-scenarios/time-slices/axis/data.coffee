d3 = require "d3"
simplify = require 'simplify-js'
modelColors = require '../../shared/colors'

ax = null
el = null

module.exports = (ax)->
  out = (data)->
    line = ax.line(type:'object')

    el = d3.select @

    sel = el.selectAll "path.data"
      .data data.profile.filter (d)->d?

    sel.enter()
      .append "path"
      .attrs
        class: "data"
        id: (d,i)->
          d.id
        d: (d)->line simplify(d,0.005,true)
        "stroke-width": 2
        stroke: (d,i)->modelColors data.rows[i]
        fill: "transparent"

  return out
