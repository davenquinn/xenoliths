d3 = require("d3")
Options = require "../../options"
Colorizer = require "../../views/base/colors"
Spine = require "spine"

Ternary = require "./ternary-axes"

class TernaryChart extends Spine.Controller
  defaults:
    margin:
      left: 50
      top: 20
      bottom: 40
      right: 0

    system: "pyroxene"
    selection: []

  constructor: ->
    super
    @margin = @margin or @defaults.margin
    @system = @defaults.system unless @system?
    @sel = @selection or []
    @colormap = new Colorizer["samples"]()
    m = @margin
    size = Math.min @el.width(), @el.height()

    @width = size - m.left - m.right
    @height = size - m.top - m.bottom
    @system = Options.systems[@system]

    @dispatcher = d3.dispatch("updated", "mouseout")

    @ternary = new Ternary
      range: [0,Math.min(@width,@height)]
      margin: [50,50]

    @setupEventHandlers()
    @drawSVG()

  drawSVG: ->
    a = this
    m = @margin
    @svg = d3.select @el[0]
      .append("svg")
        .attr
          width: @el.width()

