$ = require("jquery")
require "../../helpers/simple-slider"
GenericView = require("../base/generic")
Handlebars = require("handlebars")
Options = require("../../options")
template = require("../../templates/map/classify-options.html")
OptionsView = GenericView.extend(
  defaults:
    opacity: 0.7
    mineral: "ol"

  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    @minerals = Options["minerals"]
    @template = template
    @render()
    @opacity.bind "slider:changed", @opacityChanged
    return

  events:
    "change select[name=mineral]": "mineralChanged"
    "change input[name=opacity]": "opacityChanged"
    "change select[name=mode]": "modeChanged"
    "click button#save": "save"

  render: ->
    @$el.html @template(minerals: @minerals)
    @opacity = $("input[name=opacity]").simpleSlider(range: [
      0
      1
    ]).simpleSlider("setValue", @defaults.opacity)
    this

  mineralChanged: (event) ->
    min = $(event.currentTarget).val()
    @map.onChangeMineral min
    
    #this.parent.trigger("change:mineral",min);
    false

  modeChanged: (event) ->
    mode = $(event.currentTarget).val()
    if mode is "draw"
      @map.setDraw true
    else
      @map.setDraw false
    false

  opacityChanged: (event) ->
    @map.onChangeOpacity event.value
    
    #this.parent.trigger("change:opacity",event.value);
    false

  save: (event) ->
    @parent.onSaved()
    return
)
module.exports = OptionsView
