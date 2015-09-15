Spine = require "spine"
Selection = require "./data/selection"

class App extends Spine.Controller
  API: (o)->
    o.url = "/api"+o.url
    o.dataType ?= "json"
    if o.type == "POST"
      o.data = JSON.stringify o.data
      o.contentType = "application/json"
    return $.ajax(o)
  api: (url)->
    d3.xhr "/api"+url
      .header "X-Requested-With", "XMLHttpRequest"
      .header "Content-Type", "application/json"
      .responseType "json"
  Options: require "../options"
  Data:
    Measurement: require "./data"
  constructor: ->
    super
    window.App = @

    for f in @data.features
      new @Data.Measurement(f)
    @Data.Measurement.imported = true
    @Data.Measurement.trigger "imported"

    @selection = new Selection

    @el.append "<div />"
      .attr "id", "container"
    @routes require("./routes")
    @log "Finished setting up app"

module.exports = App
