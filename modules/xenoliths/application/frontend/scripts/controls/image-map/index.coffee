Spine = require "spine"
po = require "../../lib/polymaps"

class MapControl extends Spine.Controller
  constructor: ->
    super
    @sel = @selected
    @sel = [] unless @sel
    @_map = po.map()
      .container @el[0].appendChild(po.svg("svg"))
      .add po.interact()

    App.API
      url: "/probe-data"
      type: "GET"
      success: @addImages

  addImages: (d)=>
    console.log d

module.exports = MapControl
