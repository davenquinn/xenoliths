Backbone = require("backbone")
d3 = require("d3")
MapBase = require("./base")
Options = require("../../options")
Map = MapBase.extend(
  initialize: ->
    Map.__super__.initialize.apply this, arguments
    @parent = @options.parent
    @data = @options.data
    @sel = @options.selected
    @sel = []  unless @sel
    @setupEventHandlers()
    @colormap = new @colors["oxide_total"]()
    @addPoints @data
    return

  addPoints: (data) ->
    a = this
    @overlay = new OpenLayers.Layer.Vector("measurements")
    
    # Add the container when the overlay is added to the map.
    #this.overlay.afterAdd = this.drawSVG;
    @map.addLayer @overlay
    @drawSVG()
    return

  drawSVG: ->
    a = this
    project = (x) ->
      point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]))
      [
        point.x
        point.y
      ]

    div = d3.selectAll("#" + a.overlay.div.id)
    div.selectAll("svg").remove()
    @svg = div.append("svg").on("click", @onBackgroundClick)
    
    #.attr("width", $("#map").width())
    #.attr("height", $("#map").height());
    g = @svg.append("svg:g")
    bounds = a.getBounds(a.data)
    path = d3.geo.path().projection(project)
    
    #var ramp=d3.scale.sqrt().domain([0,10]).range(["#71eeb8","salmon"]);
    a.feature = g.selectAll(".dot").data(a.data.features).enter().append("path").attr("class", "dot").attr("d", path.pointRadius(3.5)).style("fill", a.colormap.func).on("mouseover", a.onMouseMove).on("mouseout", a.onMouseOut).on("click", a.onClick).classed("selected", (d) ->
      a.sel.indexOf(d) isnt -1
    )
    reset = ->
      bottomLeft = project(bounds[0])
      topRight = project(bounds[1])
      a.svg.attr("width", topRight[0] - bottomLeft[0]).attr("height", bottomLeft[1] - topRight[1]).style("margin-left", bottomLeft[0] + "px").style "margin-top", topRight[1] + "px"
      g.attr "transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")"
      a.feature.attr "d", path
      return

    reset()
    a.map.events.register "moveend", a.map, reset
    a.zoomToPoint @sel[0].geometry.coordinates, 4  if @sel[0]?
    return

  getBounds: (data) ->
    xvalues = []
    yvalues = []
    $.each data.features, (i, el) ->
      c = el.geometry.coordinates
      xvalues.push c[0]
      yvalues.push c[1]
      return

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

  setupEventHandlers: ->
    a = this
    @dispatcher = d3.dispatch("updated", "mouseout")
    @onMouseMove = (d, i) ->
      d3.selectAll(".dot.hovered").classed "hovered", false
      sel = d3.select(this)
      if d3.event.shiftKey and not sel.classed("selected")
        sel.classed "selected", true
        a.sel.push d
      sel.classed "hovered", true
      a.dispatcher.updated.apply this, arguments
      return

    @onMouseOut = (d, i) ->
      sel = d3.select(this)
      if a.sel.length > 0
        sel.classed "hovered", false
        a.dispatcher.mouseout.apply this, arguments
      return

    @onClick = (d, i) ->
      item = d3.select(this)
      
      #if (a.selectMode == "multiple") {
      toSelect = not item.classed("selected")
      item.classed "selected", toSelect
      if toSelect
        a.sel.push d
      else
        index = a.sel.indexOf(d)
        a.sel.splice index, 1
      a.dispatcher.updated.apply this, arguments
      
      #}
      d3.event.stopPropagation()
      return

    @onBackgroundClick = (d, i) ->
      
      #if (a.selectMode == "multiple") {
      d3.selectAll(".dot.selected").classed "selected", false
      d3.event.stopPropagation()
      a.sel.length = 0
      a.dispatcher.updated.apply this, arguments
      return

    return

  
  #}
  setColormap: (name, options) ->
    @colormap = new @colors[name](options)
    @drawSVG()
    return

  setSelectMode: (mode) ->
    @selectMode = mode
    return
)
module.exports = Map
