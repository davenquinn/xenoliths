BasePage = require "../base"
ChartPanel = require "../../controls/chart"
Sidebar = require "../../controls/sidebar"
template = require "./template.html"
ChartPage = BasePage.extend(
  initialize: (options) ->
    @options = options
    @axes =
      x: "oxides.MgO"
      y: "oxides.FeO"

    @filter = {}
    @parent = options.parent
    @compile template
    @setup()
    return

  setup: ->
    @data = App.Data.filter(@filter)
    @render()
    return

  render: ->
    @$el.height $(window).height()
    @$el.html @template
    @map = new ChartPanel(
      el: "#chart"
      parent: this
      data: @data
      axes: @axes
    )
    @sidebar = new Sidebar(
      el: "#sidebar"
      map: @map
      parent: this
      controls: [
        "data"
        "raw"
        "chart-options"
        "filter"
      ]
    )
    return

  refresh: ->
    @map.remove()
    @setup()
    @sidebar.refresh()
    return
)
module.exports = ChartPage
