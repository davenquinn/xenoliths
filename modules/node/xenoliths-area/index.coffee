d3 = require 'd3'
fs = require 'fs'
textures = require 'textures'
color = require "color"

defaults =
  color: "#91aa5f"
  interpolate: "basis"
  size: 4

module.exports = (opts={})->
  for k,v of defaults
    opts[k] = opts[k] or v

  c = color(opts.color).hexString()
  tx = textures.lines().size(opts.size).stroke(c)
  (el, lineGenerator)->
    lineGenerator.interpolate(opts.interpolate)
    el.call tx
    pth = path.join __dirname, 'xenoliths-area.json'
    _ = fs.readFileSync pth
    data = JSON.parse _
    coords = data.geometry.coordinates
    el.append 'path'
      .datum coords
      .attr
        d: (d)->lineGenerator(d)+'Z'
        fill: tx.url()
