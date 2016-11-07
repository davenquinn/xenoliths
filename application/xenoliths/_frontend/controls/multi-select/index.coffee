$ = require "jquery"
Spine = require "spine"
d3 = require "d3"

Selection = require "../../app/data/selection"
Measurement = require "../../app/data"
Options = require "../../options"

class MultiSelectControl extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @oxides = Options.oxides
    width = $("#tabs").innerWidth()

    #var height = $("#data").innerHeight()-$("#selection_type").height()-$("#tag_manager").height();
    #this.$el.height(height);
    #this.$el.css("overflow","scroll")
    @$el.css "padding-top", 20
    @svg = d3.select(@el[0])
      .append("svg")
      .attr("width", width)

    @width = width
    @color = d3.scale.category20c()

    @listenTo Selection, "add remove empty", @update

  render: (data) ->
    return unless data?
    a = this
    h = 8
    nbars = data.length
    createBar = (d, i) ->
      y = i
      group = d3.select(this)
      data = a.processData(d)
      bars = group.selectAll "rect"
        .data(data)
        .enter()
        .append "rect"
          .attr
            x: (d) -> d.off + "%"
            width: (d) -> d.w + "%"
            height: h
            y: h * i
            fill: (d, i) -> a.color i

    @bars = @svg.selectAll "g.point"
      .data data, (d) -> d.properties.id

    @bars.enter()
      .append("g")
        .attr("class", "point")
        .on "mouseover", Measurement.hovered
        .on "mouseout", Measurement.hovered
        .each createBar
    @bars.exit().remove()
    @svg.attr "height", h * nbars

  processData: (data) ->
    p = data.properties
    data = @oxides.map (id)->
      oxides: p.oxides[id] or 0
      molar: p.molar[id] or 0
      id: id

    if p.oxides.Total < 100
      ox = 100 - p.oxides.Total
      scalar = 1
    else
      ox = 0
      scalar = 100/p.oxides.Total
    data.push
      oxides: ox
      molar: 0
      id: "?"

    mode = "oxides"
    if mode == "molar" then scalar = 1
    e = 0
    cumsum = data.map (d)->
      e += d[mode]*scalar

    return data.map (d,i)->
      off: cumsum[i]
      w: d[mode]*scalar

  update: =>
    @render Measurement.selection.collection

module.exports = MultiSelectControl
