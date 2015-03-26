d3 = require "d3"
require "d3-ternary"

ChartBase = require "../chart/base"
Options = require "../../options"
Colorizer = require "../../views/base/colors"

class TernaryChart extends ChartBase
  constructor: ->
    super
    @colormap = new Colorizer["samples"]()
    @sel = @selected
    @sel = [] unless @sel
    @dispatcher = d3.dispatch "updated", "mouseout"
    @setupEventHandlers()
    @loadAxes()
    @joinData()

  loadAxes: ->
    verts = Options.systems[@system].components

    graticule = d3.ternary.graticule()
      .majorInterval(0.2)
      .minorInterval(0.05)

    resize = (t)=>
      t.fit @el.width(),@el.height()

    @ternary = d3.ternary.plot()
      .call resize
      .call d3.ternary.scalebars()
      .call d3.ternary.vertexLabels(verts)
      .call d3.ternary.neatline()
      .call graticule

    d3.select @el[0]
      .call @ternary
      .on "click", @onBackgroundClick

    $(window).on "resize", =>
      console.log "Resizing ternary"
      resize(@ternary)
      @redraw()

  joinData: ->
    @selection = @ternary.plot()
      .selectAll ".dot"
        .data @data.features

    @selection.exit().remove()
    @selection.enter()
      .append "circle"
        .attr
          class: "dot"
          r: 3.5
        .style "fill", @colormap.func
        .on "mouseover", @onMouseMove
        .on "mouseout", @onMouseOut
        .on "click", @onClick

    @redraw()

  redraw: =>
    components = Options.systems[@system].components
    accessor = (d)=>
      a = d.properties.systems[@system]
      c = components.map (i)->a[i]
      @ternary.point c

    @selection.each (d,i)->
      a = accessor(d)
      d3.select @
        .attr
          cx: a[0]
          cy: a[1]

module.exports = TernaryChart
