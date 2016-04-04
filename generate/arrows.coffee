
module.exports = (t)->
  w = t.width()
  h = t.height()

  defs = t.node().select "defs"
  defs.append "marker"
    .attr
      id: "arrow"
      viewBox:"-6 -6 12 12"
      refX:-2
      refY:0
      markerWidth: 5
      markerHeight: 5
      markerUnits: "strokeWidth"
      orient:"auto"
    .append "polygon"
      .attr
        points: "-5,5 5,0 -5,-5"
        stroke: '#000'
        fill: 'black'
        'stroke-width': '1px'

  data = [[0,h,120],[w,h,60]]

  sel = t.node().selectAll 'g.arrow'
    .data data

  g = sel.enter()
    .append 'g'
    .attr
      class: 'arrow'
      transform: (d)->
        "translate(#{d[0]} #{d[1]}) rotate(#{d[2]})"

  g.append 'line'
    .attr
      x1: 0
      x2: 10
      y1: 0
      y2: 0
      stroke: "black"
      'stroke-width': 1

  g.append 'polygon'
    .attr
      points: "-4,4 4,0 -4,-4"
      stroke: '#000'
      fill: 'black'
      'stroke-width': 0
      transform: 'translate(10 0)'




