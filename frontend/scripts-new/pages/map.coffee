$ = require "jquery"
Spacepen = require "space-pen"
Sidebar = require "../sidebar"
MapPanel = require "../controls/map"

class MapPage extends Spacepen.View
    @content: ->
        @div =>
            @div id: "main"
            @subview "sidebar", new Sidebar(["data","raw","map-options","filter"])

    initialize: (options)->
        if options?
            @sample = options.sample
        @sample = "CK-2" unless @sample?
        @filter = samples: [@sample]
        @data = window.App.Data.filter(@filter)

    afterAttach: =>
        console.log "Map page is attached"
        @height $(window).height()
        @map = new MapPanel()
        @children("#main").append @map
        window.App.State.viewer = @map

    createSelection: ->
        isSelected = (element, index, array) ->
            s = (element.properties.id is a.options.point)
            s
        isTagged = (element, index, array) ->
            ind = element.properties.tags.indexOf(a.options.tag)
            console.log ind
            ind > -1
        a = this
        selection = null
        selection = @data.features.filter(isTagged)    if @options.tag
        selection = @data.features.filter(isSelected)    if @options.point
        console.log selection
        selection

    onSampleChanged: (sample) ->
        @sample = sample
        @map.remove()
        @sidebar.refresh()
        @setup()
        return

module.exports = MapPage
