$ = require("jquery")
Spine = require "spine"
template = require("./select-map.html")

class SelectMap extends Spine.Controller
  defaults:
    sample: "CK-2"

  constructor: ->
    super
    @map = @parent.map
    @currentLayer = "sem"
    @render()

  events:
    "change select[name=sample]": "sampleChanged"
    "change .layer-switch": "changeLayer"

  render: ->
    @$el.html template samples: App.Options.samples
    @setSelected @map.sample_name

  sampleChanged: (event) ->
    smp = $(event.currentTarget).val()
    @map.parent.onSampleChanged smp

  setSelected: (sample) ->
    @$("select[name=sample]").val sample

  changeLayer: (event) ->
    val = $(event.currentTarget).val()
    lyr = (if @currentLayer is "sem" then "scan" else "sem")
    @map.setLayer lyr
    @currentLayer = lyr

module.exports = SelectMap
