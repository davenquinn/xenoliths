Options = require("../../options")
Colorizer = require("../../views/base/colors")
Spine = require "spine"
OpenLayers = window.OpenLayers

class Map extends Spine.Controller
  constructor: ->
    super
    @changeSample @sample
    @colors = Colorizer

  startMap: ->
    @bounds = OpenLayers.Bounds.fromArray(@sample.bounds)

    @map = new OpenLayers.Map
      div: @el[0]
      controls: []
      maxExtent: @bounds
      theme: null
      maxResolution: 64.000000
      numZoomLevels: 8

    @GeoJSON = new OpenLayers.Format.GeoJSON()
    @navControl = new OpenLayers.Control.Navigation()
    @map.addControls [
      new OpenLayers.Control.Zoom()
      @navControl
      new OpenLayers.Control.KeyboardDefaults()
      new OpenLayers.Control.MousePosition(numDigits: 2)
      new OpenLayers.Control.ArgParser()
    ]
    @baseLayers = {}
    @setupTiles "sem"
    @setupTiles "scan"
    @setLayer "sem"
    @map.zoomToExtent @bounds

  setupTiles: (mapType) =>
    a = @
    mapBounds = @bounds
    getURL = (bounds) ->
      mapMinZoom = 0
      mapMaxZoom = 7
      emptyTileURL = "http://www.maptiler.org/img/none.png"
      bounds = @adjustBounds(bounds)
      res = @getServerResolution()
      x = Math.round((bounds.left - @tileOrigin.lon) / (res * @tileSize.w))
      y = Math.round((bounds.bottom - @tileOrigin.lat) / (res * @tileSize.h))
      z = @getServerZoom()
      path = "/data/tiles/" + a.options.sample + "/" + mapType + "/" + z + "/" + x + "/" + y + "." + @type
      url = @url
      url = @selectUrl(path, url)  if OpenLayers.Util.isArray(url)
      if mapBounds.intersectsBounds(bounds) and (z >= mapMinZoom) and (z <= mapMaxZoom)
        url + path
      else
        emptyTileURL

    layer = new OpenLayers.Layer.TMS @sample, "",
      resolutions: [16,8,4,2,1,0.5]
      serverResolutions: [64,32,16,8,4,2,1]
      transitionEffect: "resize"
      alpha: true
      type: "png"
      getURL: getURL
      tileOrigin: new OpenLayers.LonLat.fromArray(@sample.layers[mapType])

    @baseLayers[mapType] = layer
    @map.addLayers [layer]
    layer

  changeSample: (sample) ->
    @sample = Options["samples"][sample]
    @sample_name = sample
    @startMap()
    return

  zoomToPoint: (point, level) ->
    centerPoint = new OpenLayers.LonLat(point[0], point[1])
    @map.setCenter centerPoint, level
    return

  setDraggable: (bool) ->
    if bool
      @navControl.activate()
    else
      @navControl.deactivate()

  setLayer: (layer) ->
    @map.setBaseLayer @baseLayers[layer]


module.exports = Map
