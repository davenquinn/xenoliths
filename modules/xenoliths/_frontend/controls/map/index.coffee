Spine = require "spine"
d3 = require("d3")
MapBase = require("./base")
ChartBase = require "../chart/base"
Options = require("../../options")

getBounds = (data) ->
  xvalues = []
  yvalues = []
  data.features.forEach (el) ->
    c = el.geometry.coordinates
    xvalues.push c[0]
    yvalues.push c[1]

  [
    [
      Math.min.apply(null, xvalues)
      Math.min.apply(null, yvalues)
    ]
    [
      Math.max.apply(null, xvalues)
      Math.max.apply(null, yvalues)
    ]
  ]

class DataLayer extends ChartBase
  constructor: ->
    @colormap = "oxide_total"
    super
    @loadAxes()

  loadAxes: =>

    @svg = d3.select @el[0]
      .select "svg"
      .on "click", @onBackgroundClick

    @svg.call @joinData
    @redraw()

  redraw: =>
    proj = @projection
    @selection.each (d)->
      console.log d
      p = proj d.geometry.coordinates
      d3.select @
        .attr cx: p[0], cy: p[1]

class Map extends MapBase
  constructor: ->
    super

    @overlay = new OpenLayers.Layer.Vector("measurements")
    # Add the container when the overlay is added to the map.
    #this.overlay.afterAdd = this.drawSVG;
    @map.addLayer @overlay

    @dataLayer = new DataLayer
      el: $ "#" + @overlay.div.id
      data: @data
      projection: (x) =>
        a = new OpenLayers.LonLat x[0], x[1]
        point = @map.getViewPortPxFromLonLat a
        [point.x, point.y]

    @map.events.register "moveend", @map, @dataLayer.redraw

  setData: (data)=>

  setColormap: (args...)=>@dataLayer.setColormap.apply args

module.exports = Map
