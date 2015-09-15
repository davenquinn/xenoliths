$ = require "jquery"
Spine = require "spine"
Options = require "../../options"
template = require "./template.html"

class ChangeColormap extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @el.html template oxides: Options.oxides

  events:
    "change select[name=colormap]": "changeColormap"

  changeColormap: (event) ->
    val = $(event.currentTarget).val()
    if Options.oxides.indexOf(val) > -1
      console.log val
      @map.setColormap "oxide",
        oxide: val
        data: @map.data

    else
      @map.setColormap val
    return

module.exports = ChangeColormap
