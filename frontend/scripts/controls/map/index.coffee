Spacepen = require "space-pen"
L = require "leaflet"
ImageLayer = require "./image-layer"

class MapPanel extends Spacepen.View
    @content: ->
        @div id: "map"

    initialize: (options)->
        @sample = window.App.Options.samples["CK-2"]


    afterAttach: ->
        @_map = L.map @[0]
        @setupTiles()



    setupTiles: ->
        bounds = [0.0,-8640.0,8577.0,0.0] # l b r t
        console.log "Map is set up"

        #ll = @_map.unproject([0,8640], @_map.getMaxZoom())
        #ur = @_map.unproject([8577,0], @_map.getMaxZoom())
        #@_map.setMaxBounds(new L.LatLngBounds(ll,ur))
        layer = L.tileLayer '/tiles/CK-2/sem/{z}/{x}/{y}.png',
            minZoom: 0
            maxZoom: 6
            tms: true
            noWrap: true
        layer.addTo @_map

        layer = L.tileLayer '/tiles/CK-2/scan/{z}/{x}/{y}.png',
            minZoom: 0
            maxZoom: 6
            tms: true
            noWrap: true
        layer.addTo @_map


        @_map.setView [0,0],1

    setupImage: ->
        properties =
            height: 8640
            width: 8577
        image = new ImageLayer "/tiles/CK-2/sem", properties
        image.addTo(@_map)



module.exports = MapPanel
