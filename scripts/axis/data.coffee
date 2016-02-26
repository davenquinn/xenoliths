d3 = require "d3"
simplify = require 'simplify-js'

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
      .attr
        class: "data"
        id: (d,i)->data.id[i]
        d: (d)->line simplify(d,0.005,true)
        "stroke-width": 2
        stroke: '#750000'
        fill: "transparent"

  return out
