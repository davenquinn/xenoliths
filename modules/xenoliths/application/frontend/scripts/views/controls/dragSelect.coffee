d3 = require("d3")
drag = d3.behavior.drag().on("drag", (d, i) ->
  selection = d3.selectAll(".selected")
  if selection[0].indexOf(this) is -1
    selection.classed "selected", false
    selection = d3.select(this)
    selection.classed "selected", true
  selection.attr "transform", (d, i) ->
    d.x += d3.event.dx
    d.y += d3.event.dy
    "translate(" + [
      d.x
      d.y
    ] + ")"

  
  # reappend dragged element as last 
  # so that its stays on top 
  @parentNode.appendChild this
  d3.event.sourceEvent.stopPropagation()
  return
)
DragControl = (parent, items) ->
  items.call drag
  console.log drag
  items.on "click", (d, i) ->
    e = d3.event
    g = @parentNode
    isSelected = d3.select(g).classed("selected")
    d3.selectAll(".selected").classed "selected", false  unless e.ctrlKey
    d3.select(g).classed "selected", not isSelected
    
    # reappend dragged element as last 
    # so that its stays on top 
    g.parentNode.appendChild g
    return

  
  # deselect all temporary selected state objects
  
  # inner circle inside selection frame
  
  # remove selection frame
  
  # remove temporary selection marker class
  parent.on("mousedown", ->
    d3.selectAll("g.selected").classed "selected", false  unless d3.event.ctrlKey
    p = d3.mouse(this)
    parent.append("rect").attr
      rx: 6
      ry: 6
      class: "selection"
      x: p[0]
      y: p[1]
      width: 0
      height: 0

    return
  ).on("mousemove", ->
    s = parent.select("rect.selection")
    unless s.empty()
      p = d3.mouse(this)
      d =
        x: parseInt(s.attr("x"), 10)
        y: parseInt(s.attr("y"), 10)
        width: parseInt(s.attr("width"), 10)
        height: parseInt(s.attr("height"), 10)

      move =
        x: p[0] - d.x
        y: p[1] - d.y

      if move.x < 1 or (move.x * 2 < d.width)
        d.x = p[0]
        d.width -= move.x
      else
        d.width = move.x
      if move.y < 1 or (move.y * 2 < d.height)
        d.y = p[1]
        d.height -= move.y
      else
        d.height = move.y
      s.attr d
      d3.selectAll("g.state.selection.selected").classed "selected", false
      d3.selectAll("g.state >circle.inner").each (state_data, i) ->
        d3.select(@parentNode).classed("selection", true).classed "selected", true  if not d3.select(this).classed("selected") and state_data.x - radius >= d.x and state_data.x + radius <= d.x + d.width and state_data.y - radius >= d.y and state_data.y + radius <= d.y + d.height
        return

    return
  ).on("mouseup", ->
    parent.selectAll("rect.selection").remove()
    d3.selectAll("g.state.selection").classed "selection", false
    return
  ).on "mouseout", ->
    if d3.event.relatedTarget.tagName is "HTML"
      
      # remove selection frame
      parent.selectAll("rect.selection").remove()
      
      # remove temporary selection marker class
      d3.selectAll("g.state.selection").classed "selection", false
    return

  return

module.exports = DragControl
