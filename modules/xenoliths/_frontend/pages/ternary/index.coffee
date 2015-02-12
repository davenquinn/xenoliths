Spine = require "spine"

TernaryPanel = require "../../controls/chart/ternary"
Sidebar = require "../../controls/sidebar"
template = require "../chart/template.html"

class ChartPage extends Spine.Controller
  constructor: ->
    super
    @filter = {}
    @setup()

  setup: ->
    @data = App.Data.filter(@filter)
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
