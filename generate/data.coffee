util = require './util'

color = (d)->d.color

sets =
  Quinn:
    r: 5
    fill: color
  Luffi:
    r: 3
    fill: '#666'
  other:
    r: 3
    fill: '#aaa'

labelOffsets = util.loadYaml 'label-offsets.yaml'

module.exports = (ternary, data)->
  loc = (d)->
    v = [d.ol,d.cpx,d.opx]
    ternary.point v

  ternary.plot()
    .selectAll 'circle'
    .data(data)
    .enter()
      .append 'circle'
      .attr
        class: (d)->"data #{d.source}"
        r: 2
      .each (d)->
        c = loc d
        d3.select @
          .attr sets[d.source] or sets.other
          .attr
            cx: c[0]
            cy: c[1]

  textSize = 10

  offset = (d)->
    o = labelOffsets[d.id] or {}
    [o.x or 50, -o.y or 0]

  g = ternary.plot()
    .selectAll 'g.data-label'
    .data data.filter (d)->d.source == 'Quinn'
    .enter()
    .append 'g'
      .attr
        class: 'data-label'
        transform: (d)->
          c = loc d
          "translate(#{c[0]},#{c[1]})"

  g.append 'text'
    .text (d)->d.id
    .attr
      fill: color
      transform: (d)->
        o = offset(d)
        "translate(#{o[0]},#{o[1]+textSize/2})"

  g.append 'line'
    .attr
      class: 'leader'
      stroke: color
      'stroke-width': 1.5
    .each (d)->
      o = offset(d)
      d3.select @
        .attr
          x2: o[0]-3
          y2: o[1]
