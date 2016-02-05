textures = require 'textures'
color = require "color"

c = color("#91aa5f").hexString()
module.exports =
  xenoliths: textures.lines().size(8).stroke(c)

