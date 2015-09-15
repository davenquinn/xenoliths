$ = require "jquery"
Spine = require "spine"

Options = require "../../../options"
template = require "./template.html"

class OptionsView extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @el.html template(oxides: Options.oxides)

  events:
    "change select[name=colormap]": "changeColormap"
    "click  button.axes": "changeAxes"

  render: ->
    this

  changeColormap: (event) ->
    val = $(event.currentTarget).val()
    if Options.oxides.indexOf(val) > -1
      @map.setColormap "oxide",
        oxide: val
        data: @map.data

    else
      @map.setColormap val
    return

  changeAxes: (event) ->
    axes =
      x: @$("#x-axis").val()
      y: @$("#y-axis").val()

    @map.setAxes axes
    false

module.exports = OptionsView
