Spine = require "spine"
ChartPanel = require "../../controls/chart"
Sidebar = require "../../controls/sidebar"
template = require "./template.html"
Measurement = require "../../app/data"

class ChartPage extends Spine.Controller
  constructor: ->
    super
    @axes =
      x: "oxides.MgO"
      y: "oxides.FeO"

    @filter = {}
    @setup()

  setup: ->
    @data = Measurement.filter(@filter)
    @render()

  render: ->
    @el.height $(window).height()
    @el.html template
    @map = new ChartPanel
      el: "#chart"
      parent: this
      data: @data
      axes: @axes

    @sidebar = new Sidebar
      el: "#sidebar"
      map: @map
      parent: this
      controls: [
        "data"
        "raw"
        "chart-options"
        "filter"
      ]

  refresh: ->
    @map.remove()
    @setup()
    @sidebar.refresh()

module.exports = ChartPage
