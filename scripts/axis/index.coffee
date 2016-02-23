d3 = require "d3"
createBackdrop = require "./backdrop"
plotData = require "./data"
G = require "../geometry"
textures = require '../textures'
xenolithsArea = require '../xenoliths-area'
uuid = require "uuid"
color = require "color"
axis = require "../../shared/axis"

module.exports = ->

  max = {T: 1700,z: 90}

  ax = axis()
    .size G.axis
    .margin 0


  ax.scale.x.domain [0,max.T]
  ax.scale.y.domain [max.z,0]
  ax.backdrop = (layers)->
    fn = createBackdrop ax
    el = ax.plotArea()
    fn.call el.node(), layers
  ax.plot = (data)->
    fn = plotData ax
    el = ax.plotArea()
    fn.call el.node(), data
  ax.xenolithArea = ->
    xenolithsArea ax.plotArea(), ax.line()

  ax
