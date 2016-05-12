axis = require "./axis"

module.exports = (el)->
  opts =
    max: {z: 4, T: 1}
    size: {height: 200, width: 200}
  ax = axis(opts)
  el.call(ax)

  data = ['cc','oc','ml','as'].map (d,i)->
    {z: i+1,id:d}
  ax.backdrop data

