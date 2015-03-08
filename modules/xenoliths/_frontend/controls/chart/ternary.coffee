d3 = require("d3")
Options = require "../../options"
Colorizer = require "../../views/base/colors"

Spine = require "spine"
class TernaryChart extends Spine.Controller
  defaults:
    margin:
      left: 50
      top: 20
      bottom: 40
      right: 0

    system: "pyroxene"
    selection: []

  constructor: ->
    super
    @margin = @margin or @defaults.margin
    @system = @defaults.system unless @system?
    @sel = @selection or []
    @colormap = new Colorizer["samples"]()
    m = @margin
    size = Math.min @el.width(), @el.height()

    @width = size - m.left - m.right
    @height = size - m.top - m.bottom
    @system = Options.systems[@system]
    @setupEventHandlers()
    @loadAxes()

  loadAxes: ->
    a = this
    @drawSVG()

  drawSVG: ->
    a = this
    m = @margin
    @svg = d3.select @el[0]
      .append("svg")
        .attr
          width: @el.width()
          height: @el.height()
        .append "g"
          .attr "transform", "translate(#{m.left},#{m.top})"

    sin30 = Math.pow(3, 1 / 2) / 2
    cos30 = .5
    rad = @height / 1.5
    h = @height
    c = [@width / 2, rad]
    l = [
      c[0] - rad * sin30
      c[1] + rad * cos30
    ]
    r = [
      c[0] + rad * sin30
      c[1] + rad * cos30
    ]
    t = [c[0],c[1] - rad]
    corners = [t,r,l]

    @x = (s) ->
      d = a.system.components.map (i)->s[i]
      corners[0][0] * d[0] + corners[1][0] * d[1] + corners[2][0] * d[2]

    @y = (s) ->
      d = a.system.components.map (i)->s[i]
      corners[0][1] * d[0] + corners[1][1] * d[1] + corners[2][1] * d[2]

    points = corners.reduce (p, c) -> "#{p} #{c[0]},#{c[1]}"

    @svg.append "polygon"
      .attr
        stroke: "black"
        fill: "white"
        points: points

    @points = @svg.append("g").attr("class", "data")
    @points.call @joinData, @data
    @dims = [@width,@height]

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

    @onBackgroundClick = (d, i) ->
      d3.selectAll(".dot.selected").classed "selected", false
      d3.event.stopPropagation()
      a.sel.length = 0
      a.dispatcher.updated.apply this, arguments

    @xTransform = (d) ->
      a.x d.properties.systems[a.options.system]

    @yTransform = (d) ->
      a.y d.properties.systems[a.options.system]

    @joinData = (element, data) =>
      dot = element.selectAll(".dot").data(data.features)
      dot.exit().remove()
      dot.enter()
        .append "circle"
        .attr
          class: "dot"
          r: 3.5
          cx: @xTransform
          cy: @yTransform
        .on "mouseover", @onMouseMove
        .on "click", @onClick
        .on "mouseout", @onMouseOut
        .style fill: @colormap.func

  setColormap: (name, options) ->
    @options.colormap = new Colorizer[name](options)
    @points.selectAll(".dot").style "fill", @options.colormap.func

  refresh: ->
    d3.select(@el).select("svg").remove()
    @loadAxes()

  setAxes: (axes) ->
    @axes = axes
    @refresh()

  setData: (data) ->
    @data = data
    @refresh()

module.exports = TernaryChart
