jsdom = require 'jsdom'
d3 = require 'd3'
fs = require 'fs'
Ternary = require "./ternary"

response = fs.readFileSync('/dev/stdin').toString()
data = JSON.parse response

func = (window, data)->
  svg = d3.select "body"
    .append "svg"
    .attr
      width: 500
      height: 500

  axes = svg.append 'g'
    .attr id: 'axes'
  plot = svg.append 'g'
    .attr id: 'plot'

  ternary = new Ternary
    range: [0,400]
    margin: [50,50]

  graticule = ternary.line [
      [0,0,1]
      [0,1,0]
      [1,0,0]
      [0,0,1]
    ]


  axes.append 'path'
    .attr
      d: graticule
      class: 'graticule'
      'fill-opacity': 0
      stroke: 'black'

  labels = ["cpx","opx","ol"]

  axes.selectAll ".label"
    .data labels
    .enter().append 'text'
      .attr
        class: 'label'
      .each (d,i)->
        pos = [0,0,0]
        pos[i] = 1
        pos = ternary.point pos

        d3.select @
          .text d
          .attr
            x: pos[0]
            y: pos[1]

  sel = plot.selectAll 'circle'
    .data data

  sel.enter()
    .append 'circle'
      .attr r: 5
      .each (d)->
        m = d.modes
        pos = ternary.point [m.cpx,m.opx,m.ol]
        d3.select @
          .attr
            cx: pos[0]
            cy: pos[1]
            fill: d.color
            'fill-opacity': 0.5
            stroke: d.color
            'stroke-width': 3

  d3.select("body").html()

jsdom.env "<html><body></body></html>",
  (err, window)->
    output = func(window, data)
    process.stdout.write output

