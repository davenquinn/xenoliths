Spine = require "spine"

MapPanel = require "../../controls/map"
Sidebar = require "../../controls/sidebar"
Measurement = require "../../app/data"
template = require "./template.html"

class MapPage extends Spine.Controller
  constructor: ->
    super
    @sample = "CK-2" unless @sample?
    @setup()

  setup: ->
    @filter = samples: [@sample]
    @data = Measurement.filter(@filter)
    @render()

  createSelection: ->
    isSelected = (element, index, array) ->
      s = (element.properties.id is a.options.point)
      s
    isTagged = (element, index, array) ->
      ind = element.properties.tags.indexOf(a.options.tag)
      console.log ind
      ind > -1
    a = this
    selection = null
    selection = @data.features.filter(isTagged)  if @tag
    selection = @data.features.filter(isSelected)  if @point
    selection

  render: ->
    @el.height $(window).height()
    @el.html template
    @map = new MapPanel(
      el: "#map"
      parent: this
      sample: @sample
      data: @data
      selected: @createSelection()
    )
    @sidebar = new Sidebar
      el: "#sidebar"
      parent: this
      controls: [
        "data"
        "raw"
        "map-options"
        "filter"
      ]

  onSampleChanged: (sample) ->
    @sample = sample
    @map.el.remove()
    @sidebar.refresh()
    @setup()

module.exports = MapPage
