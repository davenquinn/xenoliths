d3 = require 'd3'
axis = require "./axis"

module.exports = (el)->
  el.append 'h1'
    .text 'Legend'

  svg = el.append 'svg'

  w = 35
  opts =
    max: {z: 5, T: 1}
    size: {height: w*5, width: w}
  ax = axis(opts)
  legend = svg.append 'g'
    .attrs
      transform: "translate(5,5)"
    .call(ax)

  sz = legend.node().getBBox()
  svg.attrs height: sz.height+10

  labels = [
    'Forearc crust'
    'Oceanic crust'
    'Mantle lithosphere'
    'Asthenosphere'
    'Xenoliths area'
  ]

  ax.backdrop
    cc: 1
    oc: 2
    ml: 3
    as: 4

  txt = labels.map (d,i)->
    {
      text: d
      x: w+10
      y: ax.scale.y(i+.5)
    }

  sel = svg.selectAll 'text'
    .data txt

  sel.enter()
    .append 'text'
    .text (d)->d.text
    .attrs
      x: w+10
      y: (d)->d.y
      'font-size': 10

