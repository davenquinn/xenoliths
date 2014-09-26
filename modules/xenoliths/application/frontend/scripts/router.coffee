$ = require("jquery")
Backbone = require("backbone")
ClassifyPage = require("./views/page/classify")
MapPage = require("./views/page/map")
ChartPage = require("./views/page/chart")
IndexPage = require("./views/page/home")
TernaryPage = require("./views/page/ternary")
DataManager = require("./data")
Router = Backbone.Router.extend(
  initialize: (options) ->
    @manager = new DataManager()
    window.dataManager = @manager
    return

  routes:
    "": "index"
    "classify(/:sample)": "classify"
    "map(/:sample)(/point/:point)": "map"
    "map(/:sample)/tag(/:tag)": "map"
    chart: "chart"
    "ternary(/:system)": "ternary"

  index: ->
    new IndexPage(el: "body")
    return

  classify: (sample) ->
    new ClassifyPage(
      el: "body"
      sample: sample
    )
    return

  map: (sample, point, tag) ->
    new MapPage(
      el: "body"
      sample: sample
      point: point
      tag: tag
    )
    return

  chart: ->
    new ChartPage(el: "body")
    return

  ternary: (system) ->
    system = system or "pyroxene"
    new TernaryPage(
      el: "body"
      system: system
    )
    return
)
module.exports = Router
