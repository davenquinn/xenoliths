$ = require "jquery"
Spine = require "spine"
d3 = require "d3"

Options = require("../../options")

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
    @color = d3.scale.category20()
    return

  render: (data) ->
    return unless data?
    a = this
    h = 8
    nbars = data.length
    createBar = (d, i) ->
      y = i
      group = d3.select(this)
      data = a.processData(d)
      bars = group.selectAll("rect").data(data).enter().append("rect").attr("x", (d) ->
        d.off + "%"
      ).attr("width", (d) ->
        d.w + "%"
      ).attr("height", h).attr("y", h * i).attr("fill", (d, i) ->
        a.color i
      )
      return

    @bars = @svg.selectAll("g.point").data(data, (d) ->
      d.properties.id
    )
    @bars.enter().append("g").attr("class", "point").on("mouseover", (d, i) ->
      a.parent.update d
      return
    ).on("mouseout", (d, i) ->
      a.parent.update null
      return
    ).each createBar
    @bars.exit().remove()
    @svg.attr "height", h * nbars
    return

  processData: (data) ->
    oxides = data.properties.oxides
    ob = []
    for key of @oxides
      v = @oxides[key]
      ob.push oxides[v]
    if oxides.Total < 100
      ob.push 100 - oxides.Total
      scalar = 1
    else
      scalar = 100 / oxides.Total
      ob.push 0
    e = 0
    bb = []
    for i of ob
      val = ob[i] * scalar
      bb.push
        off: e
        w: val

      e = e + val
    bb

  update: ->
    @render @map.sel
    return

module.exports = MultiSelectControl
