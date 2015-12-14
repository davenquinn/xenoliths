fs = require 'fs'
d3 = require 'd3'
svgist = require 'svgist'
yaml = require "js-yaml"

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

margin = 5

columnWidth = sz.width/2-margin
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

  getColor = (d) -> if d.v is "un" then "" else minerals[d.v].color

  el = d3.select @
    .attr idx
    .attr
      width: w
      height: dy

  el.append 'text'
    .attr
      x: idx.x
      y: idx.y+7
    .text d.id

  rectangles = el.selectAll("path")
    .data(d.cls)
      .enter()
        .append("path")
        .attr
          d: projection
          stroke: "none"
          fill: getColor

generate = (el)->

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

  svg.attr height: Math.max(offsetY[0],offsetY[1])

svgist generate, filename: 'build/textures.svg'

