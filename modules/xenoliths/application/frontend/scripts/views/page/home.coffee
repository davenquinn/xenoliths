BasePage = require("./base")
ChartPanel = require("../chart/chart")
Sidebar = require("../../controls/sidebar")
template = require("../../templates/page/home.html")
IndexPage = BasePage.extend(
  initialize: ->
    @compile template
    @render()
    return

  render: ->
    @$el.html @template
    return
)
module.exports = IndexPage
