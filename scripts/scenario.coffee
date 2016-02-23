d3 = require "d3"
layout = require './layout'
G = require './geometry'
query = require '../shared/query'
queue = require('d3-queue').queue

# Specify layouts to use for each scenario
wide_layout = layout(3, ["small","large"])
interval = wide_layout.height()+G.section.spacing.y
offs2 = G.margin.outside + interval
offs3 = offs2 + interval

small_layout = layout(2, ["large"])

possibleLayouts =
  forearc:
    layout: wide_layout
    x: G.margin.outside
    y: offs2
  farallon:
    layout: wide_layout
    x: G.margin.outside
    y: G.margin.outside
  underplated:
    layout: small_layout
    x: G.margin.outside+wide_layout.width()-small_layout.width()
    y: offs3

class Scenario
  constructor: (@el, config, cb)->
    console.log config
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
        r.name row_id,
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

      slice.profile = rows.map (r)->
        a =
          id: r.row_id,
          profile: r.temperature.map (d,i)->
            {x: d, y: i*r.dz/1000}
        # Temporary hack or something
        return a.profile
      slice.ml = ml_depth(slice.profile)

  __setupLayout: =>
    _ = possibleLayouts[@name]
    pos = {x:_.x,y:_.y}
    @layout = _.layout
      .position pos
      .title @title
    d3.select(@el).call @layout

  __createAxes: =>
    axes = @layout.axes()
    axes.forEach (ax,i)=>
      d = @slices[i]
      ax.backdrop d
      if i == axes.length-1
        ax.xenolithArea()
      ax.plot d

module.exports = (data)->
  # Builds Scenarios
  s = (el)->
    sel = el.selectAll 'g.scenario'
      .data data
      .enter()
        .append "g"
        .attr class: 'scenario'
        .each (d)->
          new Scenario @,d

    el.attr
      height: offs3 + interval + G.margin.outside
      width: G.margin.outside*2 + wide_layout.width()
