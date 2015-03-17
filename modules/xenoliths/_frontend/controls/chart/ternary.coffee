d3 = require("d3")
Options = require "../../options"
Colorizer = require "../../views/base/colors"
Spine = require "spine"

Ternary = require "./ternary-axes"

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

    @dispatcher = d3.dispatch("updated", "mouseout")

    @ternary = new Ternary
      range: [0,Math.min(@width,@height)]
      margin: [50,50]

    @setupEventHandlers()
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
    l = [c[0]-rad*sin30,c[1]+rad*cos30]
    r = [
      c[0] + rad * sin30
      c[1] + rad * cos30
    ]
    t = [c[0],c[1] - rad]
    corners = [t,r,l]

    scales =
      top: d3

    points = corners.reduce (p, c) -> "#{p} #{c[0]},#{c[1]}"

    @svg.append "polygon"
      .attr
        stroke: "black"
        fill: "white"
        points: points

    @points = @svg.append("g").attr("class", "data")
    @points.call @joinData, @data
    @dims = [@width,@height]

  setupEventHandlers: =>
    a = @
    onMouseMove: (d, i) ->
      d3.selectAll(".dot.hovered").classed "hovered", false
      sel = d3.select(this)
      if d3.event.shiftKey and not sel.classed("selected")
        sel.classed "selected", true
        a.sel.push d
      sel.classed "hovered", true
      a.dispatcher.updated.apply this, arguments
      return

    onMouseOut: (d, i) ->
      sel = d3.select @
      if a.sel.length > 0
        sel.classed "hovered", false
        @dispatcher.mouseout.apply this, arguments

    onClick: (d, i) ->
      item = d3.select @
      toSelect = not item.classed("selected")
      item.classed "selected", toSelect
      if toSelect
        @sel.push d
      else
        index = @sel.indexOf(d)
        @sel.splice index, 1
      @dispatcher.updated.apply this, arguments
      d3.event.stopPropagation()

  onBackgroundClick: (d, i) =>
    d3.selectAll(".dot.selected").classed "selected", false
    d3.event.stopPropagation()
    @sel.length = 0
    @dispatcher.updated.apply this, arguments

  joinData: (element, data) =>
    dot = element.selectAll ".dot"
      .data data.features

    ternary = @ternary

    dot.exit().remove()
    dot.enter()
      .append "circle"
      .attr
        class: "dot"
        r: 3.5
      .each (d)->
        pt = d.properties.systems["pyroxene"]
        pos = ternary.point [pt.En,pt.Wo,pt.Fs]
        d3.select @
          .attr
            cx: pos[0]
            cy: pos[1]
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
