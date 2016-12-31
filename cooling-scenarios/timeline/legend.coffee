module.exports = (el)->
  g = el.append 'g'
    .attr
      class: 'legend'

  c = '#444'
  data = [{n:75,da:null},{n:40,da:'5,1'}]

  g.append 'text'
    .text "Model tracers"
    .attr
      'font-size': 8
      'font-weight': 'bold'
      fill: c

  it = g.selectAll 'g.item'
    .data data
    .enter()
      .append 'g'
      .attr
        class: 'item'
        transform: (d,i)->"translate(0,#{12*(i+1)})"

  it.append 'line'
    .attr
      stroke: c
      'stroke-dasharray': (d)->d.da
      x2: 17
      y1: -3
      y2: -3

  it.append 'text'
    .text (d)->"#{d.n} km depth"
    .attr
      fill: c
      x: 20
      'font-size': 8


