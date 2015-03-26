d3 = require "d3"
require "d3-ternary"

ChartBase = require "../chart/base"
Options = require "../../options"

class TernaryChart extends ChartBase
  constructor: ->
    super
    @loadAxes()
    @ternary.plot().call @joinData

  loadAxes: ->
    verts = Options.systems[@system].components

    graticule = d3.ternary.graticule()
      .majorInterval(0.2)
      .minorInterval(0.05)

    @ternary = d3.ternary.plot()
      .call d3.ternary.scalebars()
      .call d3.ternary.vertexLabels(verts)
      .call d3.ternary.neatline()
      .call graticule

    @resize()

    d3.select @el[0]
      .call @ternary
      .on "click", @onBackgroundClick

  resize: =>
    @ternary.fit @el.width(),@el.height()
    @redraw()

  redraw: =>
    components = Options.systems[@system].components
    accessor = (d)=>
      a = d.properties.systems[@system]
      c = components.map (i)->a[i]
      @ternary.point c

    return unless @selection?
    @selection.each (d,i)->
      a = accessor(d)
      d3.select @
        .attr
          cx: a[0]
          cy: a[1]

module.exports = TernaryChart
