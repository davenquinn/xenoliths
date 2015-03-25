d3 = require "d3"
require "d3-ternary"

Options = require "../../options"
Colorizer = require "../../views/base/colors"
Spine = require "spine"

class TernaryChart extends Spine.Controller
  constructor: ->
    super
    @colormap = new Colorizer["samples"]()
    @sel = @selected
    @sel = [] unless @sel
    @dispatcher = d3.dispatch "updated", "mouseout"
    @setupEventHandlers()
    @drawSVG()
    @joinData()

  drawSVG: ->
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

  setupEventHandlers: ->
    a = this
    @dispatcher = d3.dispatch("updated", "mouseout")
    @onMouseMove = (d, i) ->
      d3.selectAll(".dot.hovered").classed "hovered", false
      sel = d3.select(this)
      if d3.event.shiftKey and not sel.classed("selected")
        sel.classed "selected", true
        a.sel.push d
      sel.classed "hovered", true
      a.dispatcher.updated.apply this, arguments
      return

    @onMouseOut = (d, i) ->
      sel = d3.select(this)
      if a.sel.length > 0
        sel.classed "hovered", false
        a.dispatcher.mouseout.apply this, arguments
      return

    @onClick = (d, i) ->
      item = d3.select(this)
      toSelect = not item.classed("selected")
      item.classed "selected", toSelect
      if toSelect
        a.sel.push d
      else
        index = a.sel.indexOf(d)
        a.sel.splice index, 1
      a.dispatcher.updated.apply this, arguments
      d3.event.stopPropagation()
      return

    @onBackgroundClick = (d, i) ->
      d3.selectAll(".dot.selected").classed "selected", false
      d3.event.stopPropagation()
      a.sel.length = 0
      a.dispatcher.updated.apply this, arguments
      return

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

  setColormap: (name, options) ->
    @colormap = new Colorizer[name](options)
    @points.selectAll(".dot").style "fill", @colormap.func
    return

  refresh: ->
    d3.select(@el).select("svg").remove()
    @loadAxes()
    return

  setAxes: (axes) ->
    @axes = axes
    @refresh()
    return

  setData: (data) ->
    @data = data
    @refresh()
    return

module.exports = TernaryChart
