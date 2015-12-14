fs = require 'fs'
d3 = require 'd3'
svgist = require 'svgist'
yaml = require "js-yaml"

dpi = 72
basepath = '/Users/Daven/Development/Xenoliths/application/xenoliths/_frontend/'
appRequire = (d)->require basepath+d
options = appRequire 'options'

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

#Order down and then across
range = [2..7]
ids = ("CK-#{i}" for i in range)

margin = 5

# Tracks offset along figure axis
offsetY = 0

createView = (d,i)->
  w = sz.width/2
  # Height will be calculated automatically
  idx =
    x: 0
    y: offsetY

  cls = d.cls
  # Setup data
  width = d.shape[1]
  height = d.shape[0]

  if d.id == 'CK-3'
    width -= 10

  dy = w*height/width
  # new offset
  offsetY += dy

  x = d3.scale.linear()
    .domain([0,width])
    .range([idx.x,idx.x+w])
  y = d3.scale.linear()
    .domain([0,height])
    .range([idx.y,offsetY])

  projection = d3.geo.path()
    .projection (d)->
      [x(d[0]),y(d[1])]

  getColor = (d) -> if d.v is "un" then "" else minerals[d.v].color

  el = d3.select @
    .attr idx
    .attr
      width: w
      height: dy

  rectangles = el.selectAll("path")
    .data(cls)
      .enter()
        .append("path")
        .attr
          d: projection
          stroke: "none"
          fill: getColor

generate = (el)->

  data = JSON.parse(fs.readFileSync('build/classes.json').toString())
  imagePaths = yaml.safeLoad fs.readFileSync('images.yaml')
  data.forEach (d)->
    d.imagePath = imagePaths[d.id]
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

svgist generate, filename: 'build/textures.svg'

