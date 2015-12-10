fs = require 'fs'
d3 = require 'd3'
svgist = require 'svgist'

dpi = 72
basepath = '/Users/Daven/Development/Xenoliths/application/xenoliths/_frontend/'
appRequire = (d)->require basepath+d
options = appRequire 'options'

#Order down and then across
ids = ["CK-2","CK-5","CK-7","CK-3","CK-4","CK-6"]

createView = (d)->
  cls = d.cls
  # Setup data
  width = cls[0].length
  height = cls.length

  c = Array.prototype.concat
  data =
    w: width
    h: height
    values: c.apply([],cls)
             .map (d)-> v:d

  el = d3.select @

  el.attr "viewBox", "0 0 #{data.w} #{data.h}"

  getColor = (d) -> if d.v is "un" then "" else options.minerals[d.v].color2

  rectangles = el.selectAll("rect")
    .data(data.values)
      .enter()
        .append("rect")
        .attr
          stroke: "none"
          fill: getColor
          x: (d, i) => i % data.w
          y: (d, i) => Math.floor(i / data.w)
          width: 1
          height: 1

generate = (el)->

  data = JSON.parse(fs.readFileSync('build/classes.json').toString())

  sz =
    width: 4*dpi
    height: 6*dpi

  svg = d3.select el
    .attr sz

  sel = svg.selectAll 'g.section'
    .data data

  w = sz.width/2
  h = sz.height/3

  sel.enter()
    .append 'g'
    .attr
      class: 'section'
    .each (d,i)->
      idx =
        x: Math.floor((i/3)%2)*w
        y: i%3*h
      console.log idx
      d3.select @
        .attr idx
        .attr
          width: w
          height: h
    .each createView

svgist generate, filename: 'build/textures.svg'

