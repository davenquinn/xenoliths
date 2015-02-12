BasePage = require("../base")
template = require("./template.html")

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
