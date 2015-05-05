d3 = require "d3"

style =
  cc:
    fill: "#ffc3bd"
    stroke: "black"
    "stroke-width": 1
  oc:
    fill: "#aeb8ab"
    stroke: "#666"
    "stroke-width": 0.5
  ml:
    fill: "#b3c7b9"
  as:
    fill: "#d1ddd5"

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
    sel = ax.node()
      .selectAll 'rect.layer'
        .data layerData

    sel.enter().append "rect"
      .attr
        class: (d)->"layer #{d.id}"
        x: pos.x - margin
        y: pos.y - margin
        width: ax.width()+2*margin
        height: (d)->ax.scale.depth(d.z)- pos.y + margin
      .each (d)->
        d3.select(@).attr style[d.id]
