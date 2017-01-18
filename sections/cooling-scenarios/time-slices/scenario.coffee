d3 = require "d3"
require 'd3-selection-multi'
{db, storedProcedure} = require '../shared/database'
util = require '../shared/util'

sql = storedProcedure "#{__dirname}/model-slice.sql"

class Scenario
  constructor: (@el, config, cb)->
    for k,v of config
      if k of @
        throw "@#{k} is already defined"
      @[k] = v
    unless @id.constructor == Array
      @id = [@id]

    @__getData()
    @__setupLayout()
    @__createAxes()

  __getData: =>
    ml_depth = (profile)->
      for i in profile
        return i.z if i.T >= 1300
      return 91 # If it's too deep

    for slice in @slices
      data = [@id, slice.id]
      rows = db.query sql,data

      slice.profile = rows.map util.makeProfile
      slice.rows = rows
      slice.ml = ml_depth(slice.profile)

  __setupLayout: =>
    @layout
      .position @position
      .title @title
      .labels @labels
    d3.select(@el).call @layout

  __createAxes: =>
    axes = @layout.axes()
    axes.forEach (ax,i)=>
      d = @slices[i]
      ax.backdrop d
      ax.labels()
      if i == axes.length-1
        ax.xenolithArea()
      ax.plot d

module.exports = Scenario
