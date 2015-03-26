d3 = require("d3")
Spine = require "spine"

ChartBase = require "./base"
Colorizer = require "../../views/base/colors"
Options = require "../../options"

console.log ChartBase

class Chart extends ChartBase
  constructor: ->
    super
    @margin =
      left: 50
      top: 20
      bottom: 40
      right: 0

    @width = @el.width() - @margin.left - @margin.right
    @height = @el.height() - @margin.top - @margin.bottom
    @setupEventHandlers()
    @loadAxes()
    return

  loadAxes: ->
    a = this
    minfunc = (axes) ->
      axfunc = (d) ->
        eval "d.properties." + axes

      max = d3.max(a.data.features, axfunc)
      min = d3.min(a.data.features, axfunc)
      rng = max - min
      min - 0.02 * rng

    maxfunc = (axes) ->
      axfunc = (d) ->
        eval "d.properties." + axes

      max = d3.max(a.data.features, axfunc)
      min = d3.min(a.data.features, axfunc)
      rng = max - min
      max + 0.02 * rng

    @x = d3.scale.linear().domain([
      minfunc(@axes.x)
      maxfunc(@axes.x)
    ]).range([
      0
      this.width
    ]).nice()
    @y = d3.scale.linear()
      .domain [minfunc(@axes.y), maxfunc(@axes.y)]
      .nice()
      .range [this.height, 0]
    @xAxis = d3.svg.axis().scale(@x).orient("bottom").tickSize(-@height)
    @yAxis = d3.svg.axis().scale(@y).orient("left").ticks(5).tickSize(-@width)
    @zoomer = d3.behavior.zoom().x(@x).y(@y).scaleExtent([
      1
      40
    ]).on("zoom", @onZoom)
    @drawSVG()

  drawSVG: ->
    a = this
    @svg = d3.select @el[0]
      .append "svg"
        .attr
          width: @el.width()
          height: @el.width()
        .append "g"
          .attr "transform", "translate(#{@margin.left},#{@margin.top})"
          .call @zoomer

    @svg.append("rect").attr("id", "clip").attr("width", @width).attr("height", @height).on "click", @onBackgroundClick
    @svg.append("g").attr("class", "x axis").attr("transform", "translate(0," + @height + ")").call(@xAxis).append("text").attr("class", "label").attr("x", @width / 2).attr("y", 30).style("text-anchor", "center").text @axes.x
    @svg.append("g").attr("class", "y axis").call(@yAxis).append("text").attr("class", "label").attr("transform", "rotate(-90)").attr("y", -40).attr("x", -@height / 2).attr("dy", ".71em").style("text-anchor", "center").text @axes.y
    clip = @svg.append("defs").append("svg:clipPath").attr("id", "clip").append("svg:rect").attr("id", "clip-rect").attr("x", "0").attr("y", "0").attr("width", @width).attr("height", @height)
    @points = @svg.append("g").attr("class", "data").attr("clip-path", "url(#clip)")
    @points.call @joinData, @data
    @dims = [
      this.width
      this.height
    ]

  setupEventHandlers: ->
    super
    a = this
    @xTransform = (d) =>
      @x eval("d.properties." + @axes.x)

    @yTransform = (d) =>
      @y eval("d.properties." + @axes.y)

    @onZoom = ->
      translate = a.zoomer.translate()
      scale = a.zoomer.scale()
      tx = Math.min(0, Math.max(a.dims[0] * (1 - scale), translate[0]))
      ty = Math.min(0, Math.max(a.dims[1] * (1 - scale), translate[1]))
      a.zoomer.translate [tx,ty]
      a.svg.select(".x.axis").call a.xAxis
      a.svg.select(".y.axis").call a.yAxis
      a.svg.selectAll(".dot").attr("cx", a.xTransform).attr "cy", a.yTransform

    @joinData = (element, data) ->
      dot = element.selectAll(".dot").data(data.features)
      dot.exit().remove()
      dot.enter().append("circle").attr("class", "dot").attr("r", 3.5).attr("cx", a.xTransform).attr("cy", a.yTransform).on("mouseover", a.onMouseMove).on("click", a.onClick).on("mouseout", a.onMouseOut).style "fill", a.colormap.func
      return

    return

  setColormap: (name, options) ->
    @colormap = new Colorizer[name](options)
    @points.selectAll(".dot").style "fill", @colormap.func
    return

  refresh: =>
    d3.select(@el[0]).select("svg").remove()
    @loadAxes()
    return

  setAxes: (axes) ->
    @axes = axes
    @refresh()

module.exports = Chart
