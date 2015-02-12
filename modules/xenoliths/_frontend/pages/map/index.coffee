GenericView = require "../base"
MapPanel = require "../../controls/map"
Sidebar = require "../../controls/sidebar"
template = require "./template.html"
MapPage = GenericView.extend(
  initialize: (options) ->
    @options = options
    @sample = @options.sample
    @sample = "CK-2"  unless @sample?
    @compile template
    @setup()
    return

  setup: ->
    @filter = samples: [@sample]
    @data = App.Data.filter(@filter)
    @render()
    return

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
    selection = @data.features.filter(isTagged)  if @options.tag
    selection = @data.features.filter(isSelected)  if @options.point
    console.log selection
    selection

  render: ->
    @$el.height $(window).height()
    @$el.html @template
    @map = new MapPanel(
      el: "#map"
      parent: this
      sample: @sample
      data: @data
      selected: @createSelection()
    )
    @sidebar = new Sidebar(
      el: "#sidebar"
      parent: this
      controls: [
        "data"
        "raw"
        "map-options"
        "filter"
      ]
    )
    return

  onSampleChanged: (sample) ->
    @sample = sample
    @map.remove()
    @sidebar.refresh()
    @setup()
    return
)
module.exports = MapPage
