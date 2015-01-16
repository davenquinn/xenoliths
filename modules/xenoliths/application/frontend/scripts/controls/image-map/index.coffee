Spine = require "spine"
po = require "../../lib/polymaps"

class MapControl extends Spine.Controller
  constructor: ->
    super
    @_map = po.map()
      .container @el[0].appendChild(po.svg("svg"))
      .add po.interact()

module.exports = MapControl
