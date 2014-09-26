$ = require("jquery")
GenericView = require("../base/generic")
Options = require("../../options")
template = require("../../templates/map/select-map.html")
SelectMap = GenericView.extend(
  defaults:
    sample: "CK-2"

  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    @samples = Options["samples"]
    @compile template
    @currentLayer = "sem"
    @render()
    return

  events:
    "change select[name=sample]": "sampleChanged"
    "change .layer-switch": "changeLayer"

  render: ->
    @$el.html @template(samples: @samples)
    @setSelected @map.sample_name
    this

  sampleChanged: (event) ->
    smp = $(event.currentTarget).val()
    @map.parent.onSampleChanged smp
    return

  setSelected: (sample) ->
    @$("select[name=sample]").val sample
    return

  changeLayer: (event) ->
    val = $(event.currentTarget).val()
    lyr = (if @currentLayer is "sem" then "scan" else "sem")
    @map.setLayer lyr
    @currentLayer = lyr
    return
)
module.exports = SelectMap
