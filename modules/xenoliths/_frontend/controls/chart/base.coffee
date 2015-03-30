$ = require "jquery"
d3 = require "d3"
Spine = require "spine"
Measurement = require "../../app/data"
Selection = require "../../app/data/selection"
Colorizer = require "../../views/base/colors"
Options = require "../../options"

class ChartBase extends Spine.Controller
  constructor: ->
    for k,v of @defaults
      @[k] = v
    super
    @colormap = new Colorizer[@colormap or "samples"]()
    @sel = @selected
    @sel = []  unless @sel
    @setupEventHandlers()
    @selection = null
    $(window).on "resize", @resize

  setupEventHandlers: =>
    @listenTo Measurement, "hovered", =>
      @selection.classed "hovered", (d)->d.hovered

    @listenTo Selection, "add remove empty", =>
      @selection.classed "selected", Measurement.selection.contains

  onBackgroundClick: Measurement.selection.empty
  onClick: (d)->
    Measurement.selection.add d
    d3.event.stopPropagation()
  joinData: (element)=>
    @selection = element
      .selectAll ".dot"
        .data @data.features

    @selection.exit().remove()
    @selection.enter()
      .append "circle"
        .attr
          class: "dot"
          r: 3.5
        .style "fill", @colormap.func
        .on "mouseover", (d, i) ->
          Measurement.hovered d
          if d3.event.shiftKey
            Measurement.selection.add d

        .on "mouseout", Measurement.hovered
        .on "click", @onClick
    @redraw()

  setColormap: (name, options) ->
    @colormap = new Colorizer[name](options)
    @selection.style "fill", @colormap.func

  refresh: =>
    d3.select(@el[0]).select("svg").remove()
    @loadAxes()

  redraw: =>
    # Redraw data on move
  resize: =>
    # Event handler for resize

  loadAxes: =>
    # Create svg and append data

  setData: (data) ->
    @data = data
    @refresh()

module.exports = ChartBase

