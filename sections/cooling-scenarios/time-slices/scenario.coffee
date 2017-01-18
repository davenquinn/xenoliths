d3 = require "d3"
require 'd3-selection-multi'
{db, storedProcedure} = require '../shared/database'
util = require '../shared/util'
Promise = require 'bluebird'

sql = storedProcedure "#{__dirname}/model-slice.sql"

ml_depth = (profile)->
  for i in profile
    return i.z if i.T >= 1300
  return 91 # If it's too deep

class Scenario
  constructor: (@el, config, cb)->
    for k,v of config
      if k of @
        throw "@#{k} is already defined"
      @[k] = v
    unless @id.constructor == Array
      @id = [@id]

    @__getData()
      .tap @__setupLayout
      .then @__createAxes
      .then cb

  __getData: =>
    mapFn = (slice)=>
      data = [@id, slice.id]
      db.query sql,data
        .then (rows)->
          console.log "Getting data", rows
          slice.profile = rows.map util.makeProfile
          slice.rows = rows
          slice.ml = ml_depth(slice.profile)
          return slice

    Promise.map @slices, mapFn

  __setupLayout: =>
    @layout
      .position @position
      .title @title
      .labels @labels
    d3.select(@el).call @layout

  __createAxes: (slices)=>
    axes = @layout.axes()
    axes.forEach (ax,i)=>
      d = slices[i]
      ax.backdrop d
      ax.labels()
      if i == axes.length-1
        ax.xenolithArea()
      ax.plot d

module.exports = Scenario
