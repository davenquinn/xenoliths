$ = require("jquery")
Backbone = require("backbone")
ClassifyPage = require "./pages/classify"
MapPage = require "./pages/map"
ChartPage = require "./pages/chart"
IndexPage = require "./pages/home"
TernaryPage = require "./pages/ternary"
DataManager = require "./data"
MineralModes = require "./pages/mineral-modes"

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
    "modes": "modes"

  index: ->
    new IndexPage(el: "body")
    return

  classify: (sample) ->
    new ClassifyPage(
      el: "body"
      sample: sample
    )
    return

  modes: ->
    new MineralModes el: "body"

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
