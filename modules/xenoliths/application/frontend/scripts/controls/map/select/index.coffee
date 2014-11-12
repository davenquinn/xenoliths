$ = require("jquery")
Spine = require "spine"
Toggle = require "../../toggle"
template = require("./select-map.html")

class SelectMap extends Spine.Controller
  defaults:
    sample: "CK-2"

  constructor: ->
    super
    @map = @parent.map
    @render()

  events:
    "change select[name=sample]": "sampleChanged"

  render: ->
    @$el.html template samples: App.Options.samples
    @setSelected @map.sample_name

    @layer = new Toggle
      el: @$(".layer")
      values: ["sem","scan"]
      labels: ["SEM","Scan"]
    @listenTo @layer, "change", @layerChanged


  sampleChanged: (event) ->
    smp = $(event.currentTarget).val()
    @map.parent.onSampleChanged smp

  setSelected: (sample) ->
    @$("select[name=sample]").val sample

  layerChanged: (lyr) =>
    @map.setLayer lyr
    @currentLayer = lyr

module.exports = SelectMap
