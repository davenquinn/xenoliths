d3 = require "d3"
createBackdrop = require "./backdrop"
plotData = require "./data"
G = require "../geometry"
xenolithsArea = require '../../shared/xenoliths-area'
uuid = require "uuid"
color = require "color"
axis = require "../../shared/axis"

module.exports = ->

  max = {T: 1500,z: 90}

  ax = axis()
    .size G.axis
    .margin 0


  ax.scale.x.domain [0,max.T]
  ax.scale.y.domain [max.z,0]
  ax.backdrop = (layers)->
    fn = createBackdrop ax
    el = ax.plotArea()
    fn.call el.node(), layers

    textProps =
      'font-size': 8
      dy:'1.2em'
      'text-anchor': 'middle'
      fill: '#666666'

    # Setup labels
    sz = ax.plotArea.size()
    xax = ax.graticule()
      .append 'g'
      .attr
        class: 'xaxis'
        transform: "translate(0,#{sz.height})"
    data = [0,500,1000,1500]
    xax.selectAll 'g.tick'
      .data data
      .enter()
        .append 'g'
        .each (d,i)->
          el = d3.select @
          _ = ax.scale.x(d)
          el.attr transform: "translate(#{_},0)"

          el.append 'line'
            .attr
              stroke: '#888888'
              width: 3
              y2: 2

          t = el.append 'text'
            .text d
            .attr textProps

          if i == 0
            t.attr 'text-anchor': 'start'
          if i == data.length-1
            t.text('ºC').attr 'text-anchor': 'end'

  ax.plot = (data)->
    fn = plotData ax
    el = ax.plotArea()
    fn.call el.node(), data
  ax.xenolithArea = ->
    xa = xenolithsArea()
    xa ax.plotArea(), ax.line()

  ax
