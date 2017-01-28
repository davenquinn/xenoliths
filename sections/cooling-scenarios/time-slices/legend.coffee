d3 = require 'd3'
axis = require "./axis"
xenolithsArea = require 'xenoliths-area'

module.exports = (el)->
  el.append 'h1'
    .text 'Legend'
  el = el.append 'div'
      .attrs class: 'legend-main'

  svg = el.append 'svg'

  w = 30
  opts =
    max: {z: 5, T: 1}
    size: {height: w*5, width: w}
  ax = axis(opts)
  legend = svg.append 'g'
    .attrs
      transform: "translate(1,1)"
    .call(ax)

  sz = legend.node().getBBox()
  svg.attrs height: sz.height+2

  labels = [
    'Forearc crust'
    'Oceanic crust'
    'Mantle lithosphere'
    'Astheno-<br/>sphere'
  ]

  ax.backdrop
    cc: 1
    oc: 2
    ml: 3
    as: 4

  el = el.append 'div'
    .attrs class: 'labels'

  sel = el.selectAll 'div.label.main'
    .data labels

  sel.enter()
    .append 'div'
    .text (d)->d.text
    .attrs
      class: 'label main'
    .styles
      top: (d,i)->ax.scale.y(i)
    .html (d)->d

  tx = xenolithsArea().texture
  console.log tx
  eg = ax.plotArea()
  eg.call tx
  v1 = eg.append 'rect'
    .attrs
      x: 10
      width: 10
      y: ax.scale.y(2.8)
      height: ax.scale.y(1.6)
      fill: tx.url()

  v2 = el.append 'div'
    .html 'Crystal Knob xenolith source'
    .attrs
      class: 'label ck-source'
    .styles
      top: ax.scale.y(4.2)

  getRect = (d)->
    d.node().getBoundingClientRect()
  rects = [v1,v2].map getRect
  console.log rects

  y = ax.scale.y(4.2)
  el.append 'svg'
    .attrs
      class: 'overlay'
    .append 'line'
      .attrs
        class: 'leader'
        x1: 20
        x2: 39
        y1: y
        y2: y+6

