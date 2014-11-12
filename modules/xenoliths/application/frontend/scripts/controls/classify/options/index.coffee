$ = require("jquery")

template = require("./template.html")
Dragdealer = require("dragdealer").Dragdealer
Spine = require "spine"
Toggle = require "../../toggle"

class OptionsView extends Spine.Controller
  defaults:
    opacity: 0.7
    mineral: "ol"

  constructor: ->
    super
    @render()

  events:
    "change select[name=mineral]": "mineralChanged"
    "change select[name=mode]": "modeChanged"
    "click button#save": "save"

  render: ->
    @$el.html template
      minerals: App.Options.minerals
      opacity: @defaults.opacity

    opacity = new Dragdealer 'opacity',
      x: @defaults.opacity
      animationCallback: (x, y) =>
        @trigger "change:opacity", x
        @$('#opacity .handle').text Math.round(x * 100)+"%"

    @mode = new Toggle
      el: $(".mode")
      values: ["draw","navigate"]
      labels: ["Draw","Navigate"]
    @listenTo @mode, "change", @modeChanged

  mineralChanged: (event) ->
    min = $(event.currentTarget).val()
    @trigger "change:mineral", min

  modeChanged: (mode) =>
    draw = if mode is "draw" then true else false
    @trigger "change:draw-enabled", draw

  save: (e)-> @trigger "save"

module.exports = OptionsView
