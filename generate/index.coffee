fs = require 'fs'
d3 = require 'd3'
svgist = require 'svgist'

dpi = 72
basepath = '/Users/Daven/Development/Xenoliths/application/xenoliths/_frontend/'
appRequire = (d)->require basepath+d
options = appRequire 'options'

sz =
  width: 4*dpi
  height: 6*dpi


#Order down and then across
ids = ["CK-2","CK-5","CK-7","CK-3","CK-4","CK-6"]

createView = (d,i)->
  w = sz.width/2
  h = sz.height/3
  idx =
    x: Math.floor((i/3)%2)*w
    y: i%3*h

  el = d3.select @
    .attr idx
    .attr
      width: w
      height: h

  cls = d.cls
  # Setup data
  width = d.shape[1]
  height = d.shape[0]

  x = d3.scale.linear()
    .range([idx.x,idx.x+w])
    .domain([0,width])
  y = d3.scale.linear()
    .range([idx.y,idx.y+h])
    .domain([0,height])
  projection = d3.geo.path()
    .projection (d)->
      [x(d[0]),y(d[1])]

  getColor = (d) -> if d.v is "un" then "" else options.minerals[d.v].color2

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

