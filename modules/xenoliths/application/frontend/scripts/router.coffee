$ = require("jquery")
Backbone = require("backbone")
ClassifyPage = require("./controls/classify")
MapPage = require("./views/page/map")
ChartPage = require("./views/page/chart")
IndexPage = require("./views/page/home")
TernaryPage = require("./views/page/ternary")
DataManager = require("./data")
MineralModes = require "./pages/mineral-modes"
NewMap = require "./pages/map"

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
    "map2(/:sample)": "map2"
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

  map2: (sample)->
    new NewMap
      el: "body"
      sample: sample

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
