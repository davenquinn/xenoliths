{curveBasisClosed} = require 'd3-shape'
path = require 'path'
fs = require 'fs'
textures = require 'textures'
chroma = require "chroma-js"

defaults =
  color: "#91aa5f"
  size: 4

module.exports = (opts={})->
  for k,v of defaults
    opts[k] = opts[k] or v

  c = chroma(opts.color).css()
  tx = textures.lines().size(opts.size).stroke(c)
  fn = (el, lineGenerator)->
    lineGenerator.curve(curveBasisClosed)
    el.call tx
    pth = path.join __dirname, 'xenoliths-area.json'
    _ = fs.readFileSync pth
    data = JSON.parse _
    coords = data.geometry.coordinates
    el.append 'path'
      .datum coords
      .attr 'd', (d)->lineGenerator(d)
      .attr 'fill', tx.url()
  fn.texture = tx
  fn
