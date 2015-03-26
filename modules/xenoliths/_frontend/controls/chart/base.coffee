d3 = require "d3"
Spine = require "spine"

Colorizer = require "../../views/base/colors"
Options = require "../../options"

class ChartBase extends Spine.Controller
  constructor: ->
    super
    @colormap = new Colorizer["samples"]()
    @sel = @selected
    @sel = []  unless @sel

    @selection = null

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

  setColormap: (name, options) ->
    @colormap = new Colorizer[name](options)
    @selection.selectAll(".dot").style "fill", @colormap.func
    return

  refresh: =>
    d3.select(@el[0]).select("svg").remove()
    @loadAxes()

  setData: (data) ->
    @data = data
    @refresh()

module.exports = ChartBase

