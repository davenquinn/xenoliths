d3 = require "d3"
chroma = require 'chroma-js'

c = (d, s=.4, l=.85)->
  chroma(d)
    .set('hsl.l',l)
    .set('hsl.s',s)
    .css()

style =
  cc:
    fill: c("#f5a185")
    stroke: "#666666"
    "stroke-width": 1
  oc:
    fill: c("#4f5a78")
    stroke: "#666"
    "stroke-width": 0.5
  ml:
    fill: c("#c7d7aa", .65, .85)
  as:
    fill: c("#c7d7aa",.5,.95)

profileDepths = (profiles, temperature)->
  profiles.map (profile)->
    for loc in profile
      break if loc.x > temperature
    return loc.y

module.exports = (ax)->
  # Function that creates an axis backdrop
  maxZ = 95


  (layers)->
    pos = ax.position()
    margin = 5

    layerData = []
    # cc
    for i in ["cc","oc"]
      d = layers[i]
      continue unless d?
      layerData.push { z: d, id: i }

    # Deal with mantle lithosphere, putting it at
    # 1350ºC
    try
      depths = profileDepths(layers.profile, 1300)
        .sort()
    catch err
      depths = [layers.ml]

    allSame = depths.every (d)->d == depths[0]
    if allSame
      layerData.push {z: depths[0], id: 'ml'}
    else
      console.log depths
      scale = chroma.scale([style.ml.fill,style.as.fill])
        .domain([0,depths.length])
      depths.forEach (d,i)->
        layerData.push {z: d, style: {fill: scale(i)}}

    if depths[depths.length-1] < 90
      layerData.push {z: maxZ, id: 'as'}

    for d in layerData
      d.style = style[d.id] unless d.style?

    console.log layerData
    sel = d3.select @
      .selectAll 'rect.layer'
        .data layerData.reverse()

    sz = ax.size()

    sel.enter().append "rect"
      .attrs
        class: (d)->"layer #{d.id}"
        x: ax.scale.x(-50)
        y: ax.scale.y(-5)
        width: ax.scale.x(1900)
        height: (d)->ax.scale.y(d.z+5)
      .each (d)->
        d3.select(@).attrs d.style
