Backbone = require("backbone")
d3 = require("d3")
MapBase = require("./base")
Options = require("../../options")
ClassifyMap = MapBase.extend(
  initialize: ->
    ClassifyMap.__super__.initialize.apply this, arguments
    @parent = @options.parent
    @data = @parent.data
    @classifyLayer()
    div = d3.selectAll("#" + @overlay.div.id)
    @svg = div.selectAll("svg")
    @mineral = "na"
    return

  classifyLayer: ->
    a = this
    overlay = new OpenLayers.Layer.Vector("classify")
    
    # Add the container when the overlay is added to the map.
    overlay.afterAdd = ->
      project = (x) ->
        point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]))
        [
          point.x
          point.y
        ]

      bounds = a.bounds
      div = d3.selectAll("#" + overlay.div.id)
      div.selectAll("svg").remove()
      svg = div.append("svg")
      g = svg.append("svg:g")
      console.log a.data
      if a.data is false
        
        #build new array
        cells = 5000
        aspect_ratio = -bounds.right / bounds.bottom
        y = Math.sqrt(cells / aspect_ratio)
        x = y.toFixed(0) * aspect_ratio
        ccx = x.toFixed(0) # cell count x
        ccy = y.toFixed(0) # cell count y
        states = new Array()
        d3.range(ccx * ccy).forEach (i) ->
          states.push v: "un"
          return

        a.data =
          w: ccx
          h: ccy
          values: states
      a.mousedown = 0
      svg.attr "viewBox", "0 0 " + a.data.w + " " + a.data.h
      minerals = Options.minerals
      getColor = (d) ->
        if d.v is "un"
          ""
        else
          minerals[d.v].color

      fillOpacity = (d) ->
        if d.v is "un"
          "0.0"
        else
          "1.0"

      svg.selectAll("rect").data(a.data.values).enter().append("svg:rect").attr("stroke", "none").attr("fill", getColor).attr("fill-opacity", fillOpacity).attr("x", (d, i) ->
        i % a.data.w
      ).attr("y", (d, i) ->
        Math.floor i / a.data.w
      ).attr("width", 1).attr("height", 1).on("mousedown", (d, i) ->
        console.log a.mousedown
        if d.v is a.mineral
          d.v = "un"
        else
          d.v = a.mineral
        d3.select(this).attr("fill", getColor).attr "fill-opacity", fillOpacity
        return
      ).on "mouseover", (d, i) ->
        if d3.event.shiftKey
          d.v = a.mineral
          d3.select(this).attr("fill", getColor).attr "fill-opacity", fillOpacity
        return

      reset = ->
        bottomLeft = project([
          bounds.left
          bounds.bottom
        ])
        topRight = project([
          bounds.right
          bounds.top
        ])
        svg.attr("width", topRight[0] - bottomLeft[0]).attr("height", bottomLeft[1] - topRight[1]).style("margin-left", bottomLeft[0] + "px").style "margin-top", topRight[1] + "px"
        return

      
      #g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");
      reset()
      a.map.events.register "moveend", a.map, reset
      a.svg = svg
      return

    @map.addLayer overlay
    @overlay = overlay
    return

  onChangeOpacity: (opacity) ->
    @svg.attr "opacity", opacity
    return

  setDraw: (bool) ->
    bool = true  if bool is typeof ("undefined")
    if bool is true
      @svg.attr "pointer-events", "all"
    else
      @svg.attr "pointer-events", "none"
    return

  onChangeMineral: (mineral) ->
    @mineral = mineral
    return

  getData: ->
    @data
)
module.exports = ClassifyMap
