{curveBasisClosed} = require 'd3-shape'
path = require 'path'
fs = require 'fs'
textures = require 'textures'
chroma = require "chroma-js"

defaults =
  color: "#91aa5f"
  size: 4
  showInner: false
  strokeWidth: 1

module.exports = (opts={})->
  for k,v of defaults
    opts[k] = opts[k] or v

  c = chroma(opts.color).css()
  tx = textures.lines().size(opts.size).stroke(c)
  if opts.strokeWidth
    tx = textures.lines().strokeWidth(opts.strokeWidth).size(opts.size).stroke(c)
  if opts.showInner
    tx1 = textures.lines().strokeWidth(opts.strokeWidth*2.5).size(opts.size).stroke(c)

  fn = (el, lineGenerator)->
    lineGenerator.curve(curveBasisClosed)
    el.call tx
    pth = path.join __dirname, 'xenoliths-area.json'
    _ = fs.readFileSync pth
    data = JSON.parse _
    coords = data[0].geometry.coordinates
    el.append 'path'
      .datum coords
      .attr 'd', (d)->lineGenerator(d)
      .attr 'fill', tx.url()

    return unless opts.showInner

    el.call tx1
    {coordinates} = data[1].geometry
    el.append 'path'
      .datum coordinates
      .attr 'd', lineGenerator
      .attr 'fill', tx1.url()

  fn.texture = tx
  if tx1?
    fn.texture1 = tx1
  fn
