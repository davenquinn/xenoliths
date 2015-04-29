d3 = require "d3"
layout = require './layout'
G = require './geometry'

createAxes = (axes, data)->
  axes.forEach (ax,i)->
    console.log ax.position()
    d = data[i]
    ax.backdrop d
    if i == axes.length-1
      ax.xenolithArea()
    ax.plot d

# Specify layouts to use for each scenario
wide_layout = layout(4, ["large","small","large"])
offs2 = wide_layout.height()+G.margin.outside+G.section.spacing.y
params =
  farallon:
    layout: wide_layout
    x: G.margin.outside
    y: G.margin.outside
  monterey:
    layout: wide_layout
    x: G.margin.outside
    y: offs2
  underplating:
    layout: layout(2, ["large"])
    x: wide_layout.width()+G.section.spacing.x+G.margin.outside
    y: offs2

module.exports = (data)->
  # Builds Scenarios
  data.forEach (d)->
    for k,o of params[d.name]
      d[k] = o

  s = (el)->
    sel = el.selectAll 'g.scenario'
      .data data
      .enter().append "g"

    sel
      .attr
        class: "scenario"
      .each (d)->
        pos = {x:d.x,y:d.y}
        console.log pos
        lo = d.layout
          .position pos
          .title d.title
          .labels d.labels
        d3.select(@).call lo
        createAxes lo.axes(), d.slices

  return s
