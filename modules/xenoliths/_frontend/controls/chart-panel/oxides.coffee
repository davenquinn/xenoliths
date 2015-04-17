$ = require "jquery"
Spine = require "spine"
d3 = require("d3")

class OxidesWheel extends Spine.Controller
  constructor: ->
    super
    @mode = "oxides"
    @oxides = App.Options.oxides
    @createEventHandlers()
    @render()

  render: ->
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

    @typeLabel = @center.append("text")
      .attr
        class: "label"
        x: 0
        y: -22
      .style
        "text-anchor": "middle"
        "alignment-baseline": "middle"
        "font-size": "1em"
        "font-weight": "600"
        fill: "#888"
      .text @mode.toUpperCase()

    @el
      .css "cursor", "pointer"
      .on "click", @toggleMode

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

    @pie = d3.layout.pie()
      .value (d)=>d[@mode]
      .sort(null)

    @arc = d3.svg.arc()
      .innerRadius(@r - 85)
      .outerRadius(@r)

    arc = @arc
    @arcTween = (s) ->
      i = d3.interpolate(@_current, s)
      @_current = i(0)
      (t) -> arc i(t)

    @arcs = @svg.selectAll "path"

  toggleMode: =>
    @mode = if @mode == "molar" then "oxides" else "molar"
    @update()
    @typeLabel.text @mode.toUpperCase()
    @total.attr
      fill: if @mode == "molar" then "#aaa" else "black"

  update: (data) =>
    @data = data if data?
    @arcs = @arcs.data @processData(@data)

    arr = @oxides.concat(["?"])
    @arcs.enter()
      .append "path"
      .attr
        fill: (d, i) =>
          if i == arr.length - 1
            return "#ffffff"
          else
            return @color i
      .attr
        class: (d, i) -> arr[i]
        d: @arc
      .on "mouseover", @onMouseIn
      .on "mouseout", @onMouseOut
      .each (d) -> @_current = d

    @arcs
      .transition()
        .duration 300
        .attrTween "d", @arcTween # redraw the arcs

    @total.text @data.properties.oxides.Total.toFixed(2) + "%"
    min = App.Options.minerals[@data.properties.mineral]
    @mineral.text min.name.toUpperCase()
    color = d3.hsl(min.color)
    color.l = .3
    @mineral.style "fill", color.toString()

  createEventHandlers: ->
    a = this

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

  processData: (data) =>
    p = data.properties
    data = @oxides.map (id)->
      oxides: p.oxides[id] or 0
      molar: p.molar[id] or 0
      id: id

    ox = 0
    if p.oxides.Total < 100
      ox = 100 - p.oxides.Total

    data.push
      oxides: ox
      molar: 0
      id: "?"

    @pie data

module.exports = OxidesWheel
