$ = require "jquery"
ClassifyPage = require "../pages/classify"
MapPage = require "../pages/map"
ChartPage = require "../pages/chart"
IndexPage = require "../pages/home"
TernaryPage = require "../pages/ternary"
MineralModes = require "../pages/mineral-modes"

page_element = $ "#container"

map_route = (p) ->
  new MapPage
    el: page_element
    sample: p.sample
    point: p.point
    tag: p.tag

classify_route = (p) ->
  new ClassifyPage
    el: page_element
    sample: p.sample or null

ternary_route = (p) ->
  system = p.system or "pyroxene"
  new TernaryPage
    el: page_element
    system: system

module.exports =
  "": ->
    new IndexPage(el: page_element)

  "classify/:sample": classify_route
  "classify": classify_route
  "modes": -> new MineralModes el: page_element
  "map/:sample/point/:point": map_route
  "map/:sample/tag/:tag": map_route
  "map/:sample": map_route
  "map": map_route
  "chart": ->
    new ChartPage(el: page_element)
  "ternary": ternary_route
  "ternary/:system": ternary_route

