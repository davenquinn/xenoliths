d3 = require "d3"

style =
  cc:
    fill: "#f5a185"
    stroke: "black"
    "stroke-width": 1
  oc:
    fill: "#4f5a78"
    stroke: "#666"
    "stroke-width": 0.5
  ml:
    fill: "#c7d7aa"
  as:
    fill: "#c7d7aa"

module.exports = (ax)->
  # Function that creates an axis backdrop
  maxZ = 95

  (layers)->
    pos = ax.position()
    margin = 5

    # Set up data
    if layers.ml < 90
      layers.as = maxZ
    if layers.cc? and layers.ml < layers.cc
       delete layers.ml
    if layers.oc? and layers.ml < layers.oc
       delete layers.ml

    layerData = []
    for i in ["as","ml","oc","cc"]
      d = layers[i]
      continue unless d?
      layerData.push { z: d, id: i }

    console.log layerData
    sel = d3.select @
      .selectAll 'rect.layer'
        .data layerData

    sz = ax.size()

    sel.enter().append "rect"
      .attr
        class: (d)->"layer #{d.id}"
        x: pos.x - margin
        y: pos.y - margin
        width: sz.width+2*margin
        height: (d)->ax.scale.y(d.z)- pos.y + margin
      .each (d)->
        d3.select(@).attr style[d.id]
