
module.exports = (ternary)->
  w = ternary.width()
  h = ternary.height()

  data = [[0,h,120],[w,h,60]]

  sel = ternary.node().selectAll 'g.arrow'
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




