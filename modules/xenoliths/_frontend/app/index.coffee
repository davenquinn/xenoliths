Spine = require "spine"
Data = require "./data"

class App extends Spine.Controller
  API: (o)->
    o.url = "/api"+o.url
    o.dataType ?= "json"
    if o.type == "POST"
      o.data = JSON.stringify o.data
      o.contentType = "application/json"
    return $.ajax(o)
  Options: require "../options"
  constructor: ->
    super
    window.App = @
    console.log @data
    @Data = new Data @data
    @el.append "<div />"
      .attr "id", "container"
    @routes require("./routes")
    @log "Finished setting up app"

module.exports = App
