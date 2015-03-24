d3 = require "d3"
require "d3-ternary"

Options = require "../../options"
Colorizer = require "../../views/base/colors"
Spine = require "spine"

class TernaryChart extends Spine.Controller
  constructor: ->
    super
    @colormap = new Colorizer["samples"]()
    @sel = @selected
    @sel = [] unless @sel
    @dispatcher = d3.dispatch "updated", "mouseout"
    console.log "Setting up ternary chart"
    @drawSVG()
    @joinData()

  drawSVG: ->

    console.log @


    verts = ["Clay", "Sand", "Silt"]

    graticule = d3.ternary.graticule()
      .majorInterval(0.2)
      .minorInterval(0.05)

    resize = (t)=>
      t.fit @el.width(),@el.height()

    @ternary = d3.ternary.plot()
      .call resize
      .call d3.ternary.scalebars()
      .call d3.ternary.vertexLabels(verts)
      .call d3.ternary.neatline()
      .call graticule

    d3.select @el[0]
      .call @ternary

    $(window).on "resize", =>
      console.log "Resizing ternary"
      resize(@ternary)
      @redraw()

  joinData: ->
    a = @
    @onMouseMove = (d, i) ->
      d3.selectAll(".dot.hovered").classed "hovered", false
      sel = d3.select(this)
      if d3.event.shiftKey and not sel.classed("selected")
        sel.classed "selected", true
        a.sel.push d
      sel.classed "hovered", true
      a.dispatcher.updated.apply this, arguments
      return

    @selection = @ternary.plot()
      .selectAll ".dot"
        .data @data.features

    @selection.exit().remove()
    @selection.enter()
      .append "circle"
        .attr
          class: "dot"
          r: 3.5
        .style "fill", @colormap.func
        .on "mouseover", @onMouseMove
        #.on "click", a.onClick
        #.on "mouseout", a.onMouseOut

    @redraw()

  redraw: =>
    console.log @ternary.point
    point = @ternary.point
    @selection.each (d,i)->
      v = d.properties.systems.pyroxene
      a = point [v.En,v.Fs,v.Wo]
      d3.select @
        .attr
          cx: a[0]
          cy: a[1]


module.exports = TernaryChart
