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
wide_layout = layout(3, ["small","large"])
interval = wide_layout.height()+G.section.spacing.y
offs2 = G.margin.outside + interval
offs3 = offs2 + interval

small_layout = layout(2, ["large"])

params =
  forearc:
    layout: wide_layout
    x: G.margin.outside
    y: offs2
  farallon:
    layout: wide_layout
    x: G.margin.outside
    y: G.margin.outside
  underplating:
    layout: small_layout
    x: G.margin.outside+wide_layout.width()-small_layout.width()
    y: offs3

module.exports = (data)->
  # Builds Scenarios
  data.forEach (d)->
    for k,o of params[d.name]
      d[k] = o

  console.log data

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

    el.attr
      height: offs3 + interval + G.margin.outside
      width: G.margin.outside*2 + wide_layout.width()

  return s
