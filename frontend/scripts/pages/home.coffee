Spacepen = require "space-pen"

class Homepage extends Spacepen.View
    @content: ->
        @div id: "home", =>
            @h1 "Microprobe Data for Xenoliths"
            @h2 "Daven Quinn"
            @p "This application allows the inspection and tagging of electron microprobe data for samples gathered at Crystal Knob, in the Salinian Block."
            @h2 "Modes"
            @ul class:"links", =>
                @li =>
                    @a "Map", href: "#/map"
                @li =>
                    @a "Chart", href: "#/chart"
                @li =>
                    @a "Classify", href: "#/classify"
            @h4 "Tips"
            @p "To select points for detailed analysis (in any of the modes above), simply click the point. For multiple selections, hold down the shift key and roll over points to add to the collection."
    afterAppend: (onDom) ->
        if onDom
            console.log "On DOM"

module.exports = Homepage
