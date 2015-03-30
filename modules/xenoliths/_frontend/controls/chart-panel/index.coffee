$ = require("jquery")
OxidesWheel = require("./oxides")
MultiSelect = require("../multi-select")
TagManager = require("../tag-manager")
template = require("./chart-panel.html")
Options = App.Options
require "bootstrap-switch"
Spine = require "Spine"

Measurement = require "../../app/data"

class DataFrame extends Spine.Controller
  constructor: ->
    super
    @_d = null
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
    if Measurement.selection.collection.length > 0
      @update Measurement.selection.collection[0]
    else
      @update Measurement.collection[0]

    @listenTo Measurement, "hovered", (d) =>
      @tdata = d if d.selected()
      d = null if d == @_d
      @update d
      @_d = d

  render: -> @el.html template

  update: (data) ->
    unless data?
      @tags.update Measurement.selection.collection
      data = @tdata
    else
      @tags.update [data]
    return  unless data?
    id = data.properties.id
    sample = data.properties.sample
    @$(".id").html id
    @$(".sample").html sample
    @$(".map-link").attr "href", "#map/#{sample}/point/#{id}"
    @oxides.update data

module.exports = DataFrame
