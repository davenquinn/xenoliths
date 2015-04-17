$ = require "jquery"
Spine = require "spine"
d3 = require("d3")

class OxidesWheel extends Spine.Controller
  constructor: ->
    super
    @oxides = App.Options.oxides
    @createEventHandlers()

  render: (data) ->
    a = this
    width = $("#tabs").innerWidth()
    @parent = d3.select(@el[0])
    @r = width / 2
    @svg = @parent
      .append "svg"
        .attr
          width: width
          height: width
          viewBox: "0 0 #{width} #{width}"
          preserveAspectRatio: "xMidYMid"
        .append "g"
          .attr transform: "translate(#{@r},#{@r})"

    @center = @svg.append "g"
      .attr class: "center"

    @center.append("text")
      .attr
        class: "label"
        x: 0
        y: -22
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": "1em"
        "font-weight": "600"
        "fill ": "#888"
      .text "OXIDES"

    @mineral = @center.append "text"
      .attr
        class: "label"
        x: 0
        y: 28
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": ".8em"
        "font-weight": "600"

    @total = @center.append "text"
      .attr
        class: "label"
        x: 0
        y: 4
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": "1.8em"

    @overlay = @center.append "g"
    @overlay.append "circle"
      .attr
        r: @r - 85 - 2
        "stroke-width": 5
      .style fill: "white"

    @overlay_name = @overlay.append "text"
      .attr
        class: "label"
        x: 0
        y: 4
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": "1.9em"

    @overlay_val = @overlay.append "text"
      .attr
        class: "total"
        x: 5
        y: "1.9em"
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": "1.2em"

    @overlay.style display: "none"
    @color = d3.scale.category20c()
    @donut = d3.layout.pie().sort(null)

    arr = a.oxides.concat(["?"])

    @arc = d3.svg.arc()
      .innerRadius(@r - 85)
      .outerRadius(@r)

    @arcs = @svg.selectAll "path"
      .data(@processData(data))

    @arcs.enter()
      .append("svg:path")
      .attr
        "pointer-events": "all"
        fill: (d, i) ->
          if i == arr.length - 1
            return "#ffffff"
          else
            return a.color i
      .attr
        class: (d, i) -> arr[i]
        d: @arc
      .on "mouseover", @onMouseIn
      .on "mouseout", @onMouseOut
      .each (d) -> @_current = d

  createEventHandlers: ->
    a = this
    @update = (data) ->
      if typeof @total is "undefined"
        @render data
      else
        a = this
        @arcs = @arcs.data(@processData(data))
        @arcs.transition()
          .duration 300
          .attrTween "d", a.arcTween # redraw the arcs

      @total.text data.properties.oxides.Total.toFixed(2) + "%"
      min = App.Options.minerals[data.properties.mineral]
      @mineral.text min.name.toUpperCase()
      color = d3.hsl(min.color)
      color.l = .3
      @mineral.style "fill", color.toString()

    @arcTween = (s) ->
      i = d3.interpolate(@_current, s)
      @_current = i(0)
      (t) -> a.arc i(t)

    @onMouseIn = (d, i) ->
      el = d3.select(this)
      b = el.attr("fill")
      a.overlay
        .style display: "inherit"
        .select("circle").style "stroke", b

      a.overlay_name.text el.attr "class"
      a.overlay_val.text d.value.toFixed(2) + "%"

    @onMouseOut = (d, i) ->
      a.overlay.style "display", "none"

  processData: (data) ->
    oxides = data.properties.oxides
    ob = []
    for key of @oxides
      v = @oxides[key]
      ox = oxides[v] or 0
      ob.push ox
    if oxides.Total < 100
      ob.push 100 - oxides.Total
    else
      ob.push 0
    d = @donut(ob)
    d

module.exports = OxidesWheel
