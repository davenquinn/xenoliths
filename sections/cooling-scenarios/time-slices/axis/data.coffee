d3 = require "d3"
modelColors = require '../../shared/colors'
{textPath} = require '../../shared/util'

ax = null
el = null

module.exports = (ax)->
  out = (data)->
    console.log data
    line = ax.line(type:'object')

    el = d3.select @

    sel = el.selectAll "g.data"
      .data data.rows

    sel.enter()
      .append "g"
      .attrs
        class: "data"
      .call textPath (d)->line(d.profile)
      .select 'use'
      .attrs
        "stroke-width": 2
        stroke: modelColors
        fill: "transparent"

  return out
