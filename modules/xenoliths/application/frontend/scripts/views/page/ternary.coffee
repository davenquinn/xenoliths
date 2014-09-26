BasePage = require("./base")
TernaryPanel = require("../chart/ternary")
Sidebar = require("../base/sidebar")
template = require("../../templates/page/chart.html")
ChartPage = BasePage.extend(
  initialize: (options) ->
    @options = options
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
    @map = new TernaryPanel(
      el: "#chart"
      parent: this
      data: @data
      system: @options.system
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
