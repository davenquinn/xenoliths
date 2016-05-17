d3 = require 'd3'
axis = require "./axis"

module.exports = (el)->

  w = 35
  opts =
    max: {z: 5, T: 1}
    size: {height: w*5, width: w}
  ax = axis(opts)
  el.call(ax)

  labels = [
    'Forearc\ncrust'
    'Oceanic\ncrust'
    'Mantle\nlithosphere'
    'Asthenosphere'
    'Xenoliths\narea'
  ]

  ax.backdrop
    cc: 1
    oc: 2
    ml: 3
    as: 4


  txt = []
  labels.forEach (d,i)->
    d.split('\n').forEach (t,j)->
      txt.push
        text: t
        x: w+8
        y: ax.scale.y(i)+w/2+4+12*(j-0.5)

  sel = el.selectAll 'text.label'
    .data txt

  sel.enter()
    .append 'text'
    .text (d)->d.text
    .attr
      x: (d)->d.x
      y: (d)->d.y
      'font-size': 10

