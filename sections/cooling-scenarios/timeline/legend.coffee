textures = require 'textures'

tex = textures.lines()
        .orientation('5/8')
        .size 4
        .strokeWidth 0.5
        .stroke '#aaa'

module.exports = (el)->
  g = el.append 'g'
    .attrs
      class: 'legend'

  c = '#444'
  data = [{n:75,da:null},{n:40,da:'5,1'}]

  g.append 'text'
    .html "<tspan class='title'>Model tracers</tspan> <tspan dx=5>Final depth</tspan>"

  it = g.selectAll 'g.item'
    .data data
    .enter()
      .append 'g'
      .attrs
        class: 'item'
        transform: (d,i)->"translate(0,#{12*(i+1)})"

  it.append 'line'
    .attrs
      'stroke-dasharray': (d)->d.da
      x2: 50
      y1: -3
      y2: -3

  it.append 'text'
    .text (d)->"#{d.n} km"
    .attrs x: 82, 'text-anchor': 'end', class: 'subtitle'

  ### Texture ###

  el.call tex
  g.append 'rect'
    .attrs width: 15, height: 15, transform: 'translate(0, 44)'
    .attrs fill: tex.url(), stroke: '#aaa', 'stroke-width': 0.5


  g.append 'text'
    .attrs transform: "translate(0, 38)"
    .html "<tspan class='title'>Subduction phase</tspan>"
    .attrs 'text-anchor': 'start'

  g.append 'text'
    .attrs transform: "translate(0, 50)", class: 'axis-description'
    .html "
      <tspan x=20>Advection of model domain from</tspan>
      <tspan dy=8 x=20>0 to 30 km depth beneath forearc crust</tspan>"
    .attrs 'text-anchor': 'start'
