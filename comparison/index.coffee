yaml = require "js-yaml"
d3 = require 'd3'
fs = require 'fs'
svgist = require 'svgist'
path = require 'path'
simplifiedLine = require '../scripts/simplified-line'
xenolithsArea = require '../scripts/xenoliths-area'
textures = require '../scripts/textures'

# Create dataset from inputs
dir = fs.readFileSync('/dev/stdin').toString()
cfg = yaml.safeLoad fs.readFileSync('scenarios.yaml')
cfg = JSON.parse(JSON.stringify(cfg))

getProfile = (fn)->
  # Gets the vertical profile, zipping for friendliness
  console.log "Getting profile for", fn
  p = require fn
  return p.z.map (d,i)->{T: p.T[i], z: d*0.001}

# Build data
data = []
for c in cfg
  if not Array.isArray(c.id)
    c.id = [c.id]
  for id in c.id
    d =
      id: id
      path: path.join dir, id, 'final.json'
    data.push d

data.forEach (d)->
  d.profile = getProfile d.path

# Figure s at 100 ppi
ppi = 100

func = (el)->

  size =
    height: 4*ppi
    width: 4.5*ppi
  margin = 0.3*ppi

  plotSize =
    height: size.height-margin*2
    width: size.width-margin*2

  el = d3.select(el)
    .attr size

  defs = el.append 'defs'

  defs.append 'rect'
    .attr plotSize
    .attr
      id: 'plotArea'
      x: 0
      y: 0

  defs
    .append 'clipPath'
      .attr id: 'plotClip'
      .append 'use'
        .attr 'xlink:href': "#plotArea"

  el.call textures.xenoliths

  g = el.append 'g'
    .attr
      transform: "translate(#{margin},#{margin})"
    .attr plotSize

  ax = g.append 'g'
    .attr 'clip-path': 'url(#plotClip)'

  g.append 'use'
    .attr
      'xlink:href': "#plotArea"
      stroke: 'black'
      fill: 'transparent'

  y = d3.scale.linear()
        .domain [40,90]
        .range [0,plotSize.height]

  x = d3.scale.linear()
    .domain [900,1100]
    .range [0,plotSize.width]

  sel = ax.selectAll 'path'
    .data data.map (d)-> d.profile

  sel.enter()
    .append 'path'
    .attr
      stroke: 'grey'
      fill: 'transparent'
      d: simplifiedLine {temp: x, depth: y}, 0.005

  line = d3.svg.line()
    .x (d)->x(d[0])
    .y (d)->y(d[1])
    .interpolate 'basis'
  xenolithsArea ax, line


svgist func, filename: 'build/comparison.svg'
