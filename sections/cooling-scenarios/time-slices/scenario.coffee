d3 = require "d3"
query = require '../shared/query'
queue = require('d3-queue').queue
util = require '../shared/util'

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
    sql = "SELECT
        r.name,
        r.type,
        r.subduction_time,
        r.underplating_duration,
      	p.name profile_id,
      	p.temperature,
      	p.dz,
      	p.time
    	FROM
    	thermal_modeling.model_profile p
    	JOIN thermal_modeling.model_run r
    		ON r.id = p.run_id
    	WHERE r.name = ANY($1::text[])
        AND p.name = $2::text
      ORDER BY p.time DESC"

    ml_depth = (profile)->
      for i in profile
        return i.z if i.T >= 1300
      return 91 # If it's too deep

    for slice in @slices
      data = [@id, slice.id]
      rows = query sql,data

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
