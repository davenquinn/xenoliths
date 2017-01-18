module.exports = (el)->
  g = el.append 'g'
    .attrs
      class: 'legend'

  c = '#444'
  data = [{n:75,da:null},{n:40,da:'5,1'}]

  g.append 'text'
    .text "Model tracers"
    .attrs
      'font-size': 8
      'font-weight': 'bold'
      fill: c

  it = g.selectAll 'g.item'
    .data data
    .enter()
      .append 'g'
      .attrs
        class: 'item'
        transform: (d,i)->"translate(0,#{12*(i+1)})"

  it.append 'line'
    .attrs
      stroke: c
      'stroke-dasharray': (d)->d.da
      x2: 17
      y1: -3
      y2: -3

  it.append 'text'
    .text (d)->"#{d.n} km depth"
    .attrs
      fill: c
      x: 20
      'font-size': 8


