Spine = require "spine"
SelectMap = require "../select"
ChangeColormap = require "../../change-colormap"

class MapOptions extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @el.html "<div id=\"select-map\"></div><div id=\"colormap\"></div>"
    new SelectMap
      el: "#select-map"
      parent: @parent

    new ChangeColormap
      el: "#colormap"
      parent: @parent

module.exports = MapOptions
