$ = require "jquery"
Spine = require "spine"
template = require "./template.html"

Controls =
  raw:
    name: "Raw"
    obj: require "../raw-data"
  "chart-options":
    name: "Options"
    obj: require "../chart/options"
  "map-options":
    name: "Options"
    obj: require "../map/options"
  data:
    name: "Data"
    obj: require "../chart-panel"
  filter:
    name: "Filter"
    obj: require "../filter"

class Sidebar extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @activeTab = "#" + @controls[0]
    @render()

  render: ->
    controls = []
    for c of @controls
      id = @controls[c]
      control = {}
      control = Controls[id]
      control.id = id
      controls.push control
    opts = controls: controls

    @el.html template(opts)

    for c of controls
      control = controls[c]
      control = new control.obj
        el: "#" + control.id
        parent: this
        map: @map

    @viewTab @activeTab
    return

  refresh: ->
    for c of @controls
      @controls[c].remove()
    @render()
    return

  events:
    "click .navbar-nav a": "onNav"

  onNav: (event) ->
    val = event.currentTarget.hash
    @activeTab = val
    @viewTab val
    event.preventDefault()
    false

  viewTab: (tab) ->
    @$(".navbar-nav li").removeClass "active"
    @$("#tabs>div").hide()
    @$("a[href=" + tab + "]").parent().addClass "active"
    $(tab).show()

module.exports = Sidebar
