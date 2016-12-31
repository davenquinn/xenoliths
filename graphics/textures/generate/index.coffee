fs = require 'fs'
d3 = require 'd3'
savage = require 'savage-svg'
yaml = require "js-yaml"
global.d3 = d3
legend = require 'd3-svg-legend/no-extend'

dpi = 72

sz =
  width: 4*dpi
  height: 8*dpi

minerals =
  cpx:
    name: "Clinopyroxene"
    color: "#009245"
  opx:
    name: "Orthopyroxene"
    color: "#8CC63F"
  ol:
    name: "Olivine"
    color: "#D6E9FF"
  sp:
    name: "Spinel"
    color: "#663300"
  al:
    name: "Alteration"
    color: "#888888"
  na:
    name: "None"
    color: "#ffffff"

colorScale = d3.scale.ordinal()
  .domain (k for k,v of minerals)
  .range (v.color for k,v of minerals)

margin = 5

columnWidth = (sz.width-margin)/2
# Tracks offset along figure axis
offsetY = [margin,margin]

createView = (d,i)->
  w = columnWidth
  # Height will be calculated automatically
  columnIndex = Math.floor(i/3)

  # Text area height
  headerHeight = 10

  idx =
    x: columnIndex*(w+margin)
    y: offsetY[columnIndex]

  # Setup data
  width = d.shape[1]
  height = d.shape[0]

  if d.id == 'CK-3'
    width -= 10

  dy = w*height/width
  # new offset
  offsetY[columnIndex] += headerHeight + dy + margin

  ofs = idx.y + headerHeight
  x = d3.scale.linear()
    .domain([0,width])
    .range([idx.x,idx.x+w])
    .clamp true
  y = d3.scale.linear()
    .domain([0,height])
    .range([ofs,ofs+dy])
    .clamp true

  projection = d3.geo.path()
    .projection (d)->
      [x(d[0]),y(d[1])]

  el = d3.select @
    .attr idx
    .attr
      width: w
      height: dy

  text = el.append 'text'
    .attr
      x: idx.x
      y: idx.y+7
    .text d.id
    .style 'font-weight','500'

  rectangles = el.selectAll("path")
    .data(d.cls)
      .enter()
        .append("path")
        .attr
          d: projection
          stroke: "none"
          fill: (d)->colorScale(d.v)

generate = (el, window)->

  data = JSON.parse(fs.readFileSync('build/classes.json').toString())
  data = data.sort (a,b)->d3.ascending(a.id,b.id)

  svg = d3.select el
    .attr sz

  sel = svg.selectAll 'g.section'
    .data data

  sel.enter()
    .append 'g'
    .attr
      class: 'section'
    .each createView

  i = 0
  if offsetY[1] < offsetY[0]
    i = 1
  ofs = offsetY[i]
  legend = svg.append 'g'
    .attr
      class: 'legend'
      transform: "translate(0 #{offsetY[i]})"

  minData = (v for k,v of minerals)
  sel = legend.selectAll 'g.mineral'
    .data minData.filter (d)->d.name != 'None'
    .enter()

  sel.append 'g'
    .attr
      class: 'mineral'
    .each (d,i)->
      y = 16*i
      h = 12
      sel = d3.select @
      sel.append 'rect'
        .attr
          height: h
          width: h
          transform: "translate(0 #{y})"
          fill: d.color
      sel.append 'text'
        .text d.name
        .attr
          'dominant-baseline': 'middle'
          transform: "translate(16 #{y+h-2})"
        .style
          'font-size': 9

  sb = legend.append 'g'
    .attr
      class: 'scalebar'
      transform: "rotate(-90 #{columnWidth},0) translate(#{columnWidth/2} 0)"
  sb.append 'line'
    .attr
      x1: columnWidth/2
      stroke: 'black'
      'stroke-width': 3
  sb.append 'text'
    .text '1 cm'
    .attr
      'text-anchor': 'middle'
      transform: "translate(#{columnWidth/4} -3)"

  svg.attr height: Math.max(offsetY[0],offsetY[1])

savage generate, filename: 'build/textures.svg'

