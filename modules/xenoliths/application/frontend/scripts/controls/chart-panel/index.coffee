$ = require("jquery")
OxidesWheel = require("./oxides")
MultiSelect = require("../../views/controls/multi-select")
TagManager = require("../tag-manager")
template = require("./chart-panel.html")
Options = App.Options
require "bootstrap-switch"
Spine = require "Spine"

class DataFrame extends Spine.Controller
  constructor: ->
    super
    @render()
    @oxides = new OxidesWheel
      el: $("#oxides")
      parent: this

    @tags = new TagManager
      el: $("#tag_manager")
      parent: this

    @multiSelect = new MultiSelect
      el: $("#multiple")
      parent: this

    @tdata = null
    if @map.sel
      @update @map.sel[0]
    else
      @update @map.data.features[0]
    a = @
    @map.dispatcher.on "updated.data", (d) ->
      sel = d3.select @
      a.tdata = d  if sel.classed("selected")
      a.update d

    @map.dispatcher.on "mouseout", (d) =>
      sel = d3.select @
      a.update null

  render: -> @$el.html template

  update: (data) ->
    unless data?
      @tags.update @map.sel
      data = @tdata
    else
      @tags.update [data]
    @multiSelect.update @map.sel
    return  unless data?
    id = data.properties.id
    sample = data.properties.sample
    @$(".id").html id
    @$(".sample").html sample
    @$(".map-link").attr "href", "#map/#{sample}/point/#{id}"
    @oxides.update data

module.exports = DataFrame
