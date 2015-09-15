Spine = require "spine"

TernaryPanel = require "../../controls/ternary"
Sidebar = require "../../controls/sidebar"
Measurement = require "../../app/data"
template = require "../chart/template.html"

class ChartPage extends Spine.Controller
  constructor: ->
    super
    @filter = {}
    @setup()

  setup: ->
    @data = Measurement.filter(@filter)
    console.log @data
    @log "Rendering ternary panel"
    @render()

  render: ->
    @el.height $(window).height()
    @el.html template

    @map = new TernaryPanel
      el: "#chart"
      parent: this
      data: @data
      system: @system

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
