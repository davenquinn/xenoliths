axis = require "./axis"

module.exports = (el)->
  opts =
    max: {z: 5, T: 1}
    size: {height: 120, width: 40}
  ax = axis(opts)
  el.call(ax)

  labels = [
    'Forearc crust'
    'Oceanic crust'
    'Mantle lithosphere'
    'Asthenosphere'
  ]

  ax.backdrop
    cc: 1
    oc: 2
    ml: 3
    as: 4

