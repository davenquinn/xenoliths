d3 = require 'd3'
fs = require 'fs'
textures = require './textures'

module.exports = (el, lineGenerator)->
  _ = fs.readFileSync 'xenoliths-area.json'
  data = JSON.parse _
  coords = data.geometry.coordinates
  el.append 'path'
    .datum coords
    .attr
      d: (d)->lineGenerator(d)+'Z'
      fill: textures.xenoliths.url()
