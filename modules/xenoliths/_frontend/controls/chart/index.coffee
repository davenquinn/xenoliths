d3 = require("d3")

ChartBase = require "./base"

class Chart extends ChartBase
  constructor: ->
    super
    @margin =
      left: 50
      top: 20
      bottom: 40
      right: 0

    @loadAxes()

  loadAxes: =>

    minfunc = (axes) =>
      axfunc = (d) ->
        eval "d.properties." + axes

      max = d3.max(@data.features, axfunc)
      min = d3.min(@data.features, axfunc)
      rng = max - min
      min - 0.02 * rng

    maxfunc = (axes) =>
      axfunc = (d) ->
        eval "d.properties." + axes

      max = d3.max(@data.features, axfunc)
      min = d3.min(@data.features, axfunc)
      rng = max - min
      max + 0.02 * rng

    @x = d3.scale.linear()
      .domain [minfunc(@axes.x), maxfunc(@axes.x)]
      .nice()

    @y = d3.scale.linear()
      .domain [minfunc(@axes.y), maxfunc(@axes.y)]
      .nice()

    @xAxis = d3.svg.axis()
      .scale @x
      .orient "bottom"
      .ticks 10

    @yAxis = d3.svg.axis()
      .scale @y
      .orient "left"
      .ticks 10

    @zoomer = d3.behavior.zoom()
      .scaleExtent [1,40]
      .x @x
      .y @y
      .on "zoom", @onZoom

    @drawSVG()

  drawSVG: =>
    @svg = d3.select @el[0]
      .append "svg"
        .append "g"
          .call @zoomer

    @background = @svg.append "rect"
      .attr
        class: "background"
        fill: "white"
        x: 0
        y: 0

    @clip = @svg.append "defs"
      .append "svg:clipPath"
      .attr id: "clip"
      .append "svg:rect"
        .attr
          id: "clip-rect"
          x: 0
          y: 0

    @ax_x = @svg.append "g"
      .attr class: "x axis"
      .call @xAxis

    @ax_y = @svg.append "g"
      .attr class: "y axis"
      .call @yAxis

    @ax_x.append "text"
      .attr
        class: "label"
        x: "50%"
        y: 30
      .style "text-anchor", "center"
      .text @axes.x

    @ax_y.append "text"
      .attr
        class: "label"
        transform: "rotate(-90)"
        x: "50%"
        y: -40
        dy: ".71em"
      .style "text-anchor", "center"
      .text @axes.y

    @resize()

    @dataFrame = @svg.append "g"
      .attr
        class: "data"
        "clip-path": "url(#clip)"
      .call @joinData
      .on "click", @onBackgroundClick

  resize: =>
    console.log "Resizing"
    w = @el.width()
    h = @el.height()

    @$ "svg"
      .width w
      .height h

    @size =
      width: w - @margin.left - @margin.right
      height: h - @margin.top - @margin.bottom

    @x.range [0,@size.width]
    @y.range [@size.height, 0]

    @clip.attr @size
    @background.attr @size

    @svg
      .attr @size
      .attr transform: "translate(#{@margin.left},#{@margin.top})"

    @zoomer
      .x @x
      .y @y

    @xAxis.tickSize -@size.height
    @yAxis.tickSize -@size.width

    @ax_x
      .attr transform: "translate(0,#{@size.height})"
      .call @xAxis
    @ax_y.call @yAxis

  redraw: =>
    console.log "Drawing data"
    xt = (d)=>
      @x eval("d.properties." + @axes.x)
    yt = (d)=>
      @y eval("d.properties." + @axes.y)
    @selection.attr
      cx: xt
      cy: yt

  onZoom: =>
    translate = @zoomer.translate()
    scale = @zoomer.scale()

    offs = [@size.width,@size.height].map (d,i)->
      Math.min 0, Math.max(d*(1 - scale), translate[i])

    @zoomer.translate offs
    @svg.select(".x.axis").call @xAxis
    @svg.select(".y.axis").call @yAxis
    @redraw()

  setAxes: (axes) ->
    @axes = axes
    @refresh()

module.exports = Chart
