chroma = require 'chroma-js'

scales =
  farallon: -> chroma('darkblue')
  'farallon-reheated': chroma
    .scale ['darkblue','purple']
    .domain [-2,6]
  forearc: chroma
    .scale ['teal','limegreen']
    .domain [70,30]
  underplated: chroma
    .scale ['orange','red']
    .domain [0,6]

modelColors = (d)->
  t = d.type
  scale = scales[t]
  if t == 'forearc'
    arg = d.subduction_time
  else
    arg = d.underplating_duration
  scale(arg)

modelColors.scales = scales

module.exports = modelColors
