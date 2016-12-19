jsdom = require 'jsdom'
d3 = require 'd3'
fs = require 'fs'
pd = require 'pretty-data'

global.d3 = d3

require 'd3-ternary'

# Create dataset from inputs
data = JSON.parse(fs.readFileSync('/dev/stdin').toString())

# Figure s at 100 ppi
graticule = d3.ternary.graticule()
  .majorInterval(0.2)
  .minorInterval(0.1)

ternary = d3.ternary.plot()
  .call d3.ternary.scalebars()
  .call d3.ternary.vertexLabels(["FeO","Alkali", "MgO"])
  .call d3.ternary.neatline()
  .call graticule
  .radius 200

createTernary = (el)->
  el.call ternary

  t = ternary.node()

  t.select(".neatline")
    .attr
      fill: "none"
      stroke: "black"
      "stroke-width": 2

  t.selectAll "text"
    .attr
      "font-family": "Helvetica Neue"

  t.selectAll ".bary-axis .domain"
    .attr
      fill: "none"

  t.selectAll ".tick text"
    .attr "font-size", 10

  t.selectAll ".tick line"
    .attr
      stroke: "#eee"
      "stroke-width": 1.5

  t.selectAll ".graticule path"
    .attr
      stroke: "#eee"
      "stroke-width": 0.5

  t.selectAll ".graticule path.major"
    .attr "stroke-width": 1.5

  sel = ternary.plot()
    .selectAll ".measurement"
    .data data.molar

  sel.enter()
    .append "circle"
      .attr
        class: "measurement"
        r: 2
        fill: "#666666"
      .each (d)->
        a = [d.FeO,d.MgO,d.Na2O+d.K2O]
        pt = ternary.point a
        d3.select @
          .attr
            cx: pt[0]
            cy: pt[1]

func = (window)->
  body = window.document.querySelector("body")

  el = d3.select body

  el
    .call createTernary
    .select "svg"
    .attr xmlns: "http://www.w3.org/2000/svg"

  el.html()

jsdom.env
  html: "<html><body></body></html>"
  features:
    QuerySelector: true
  done: (err, window)->
    output = func(window)
    fs.writeFileSync data.outfile, pd.pd.xml(output)


