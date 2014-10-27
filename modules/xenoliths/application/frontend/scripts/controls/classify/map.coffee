d3 = require("d3")
MapBase = require("../map/base")
Options = require("../../options")

getShape = (bounds, n_cells=5000)->
    # Gets the shape of an array that fits
    aspect_ratio = -bounds.right / bounds.bottom
    y = Math.sqrt(n_cells / aspect_ratio)
    out =
        x: Math.round(y * aspect_ratio)
        y: Math.round(y)

class ClassifyMap extends MapBase
    constructor: ->
        super
        @data = @setupData(@parent.data)

        @classifyLayer()
        div = d3.selectAll("#" + @overlay.div.id)
        @svg = div.selectAll("svg")
        @mineral = "na"

    setupData: (data) ->
        width = data[0].length
        height = data.length
        shape = getShape(@bounds)
        console.assert(width == shape.x)
        console.assert(height == shape.y)

        ret =
            w: width
            h: height
            values: Array.prototype.concat.apply([],data).map (d)-> v:d

    classifyLayer: ->
        overlay = new OpenLayers.Layer.Vector("classify")
        a = @
        # Add the container when the overlay is added to the map.
        overlay.afterAdd = =>
            project = (x)=>
                point = @map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]))
                [point.x,point.y]

            bounds = @bounds
            div = d3.selectAll("#" + overlay.div.id)
            div.selectAll("svg").remove()
            svg = div.append("svg")
            g = svg.append("svg:g")
            if @data is false
                #build new array
                cells = 5000
                shp = getShape(@bounds)
                states = new Array()
                d3.range(shp.x * shp.y).forEach (i) ->
                    states.push v:"un"

                @data =
                    w: shp.x
                    h: shp.y
                    values: states
            @mousedown = 0
            svg.attr "viewBox", "0 0 #{@data.w} #{@data.h}"

            getColor = (d) -> if d.v is "un" then "" else App.Options.minerals[d.v].color
            fillOpacity = (d) -> if d.v is "un" then "0.0" else "1.0"

            rectangles = svg.selectAll("rect")
                .data(@data.values)
                    .enter()
                        .append("rect")
                        .attr
                            stroke: "none"
                            fill: getColor
                            "fill-opacity": fillOpacity
                            x: (d, i) => i % @data.w
                            y: (d, i) => Math.floor(i / @data.w)
                            width: 1
                            height: 1
                        .on "mousedown", (d, i) ->
                            if d.v is a.mineral
                                v = "un"
                            else
                                v = a.mineral
                            a.data.values[i].v = v
                            d3.select(@).attr
                                fill: (d)->getColor(d)
                                "fill-opacity": fillOpacity
                        .on "mouseover", (d, i) ->
                            if d3.event.shiftKey
                                a.data.values[i].v = a.mineral
                                d3.select(@).attr
                                    fill: getColor
                                    "fill-opacity": fillOpacity

            reset = ->
                bottomLeft = project [bounds.left, bounds.bottom]
                topRight = project [bounds.right, bounds.top]
                svg.attr
                  width: topRight[0] - bottomLeft[0]
                  height: bottomLeft[1] - topRight[1]
                svg.style
                  "margin-left": "#{bottomLeft[0]}px"
                  "margin-top": "#{topRight[1]}px"

            reset()
            @map.events.register "moveend", @map, reset
            @svg = svg
            return
        @map.addLayer overlay
        @overlay = overlay
        return


    setDraw: (bool) ->
        bool = true if bool is typeof ("undefined")
        if bool is true
            @svg.attr "pointer-events", "all"
        else
            @svg.attr "pointer-events", "none"

    setOpacity: (d) -> @svg.attr "opacity", d
    setMineral: (d) -> @mineral = d

    getData: ->
        # split data into n columns.
        d = @data.values.map (d)->d.v
        return (d.splice(0, @data.w) while d.length)

module.exports = ClassifyMap
