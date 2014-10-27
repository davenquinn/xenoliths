$ = require("jquery")

App =
    JSON_RPC: (method, params, callback) ->
        console.log "Invalid JSON_RPC request", method, params, callback
    API: (o)->
        o.url = "/api"+o.url
        o.dataType ?= "json"
        if o.type == "POST"
          o.data = JSON.stringify o.data
          o.contentType = "application/json"
        return $.ajax(o)
    require: (s)-> require __dirname+"/"+s

startApp = (data) ->
    window.App = App

    Backbone = require("backbone")
    Router = require("./router")
    Data = require("./data")

    App.Data = new Data(data)
    App.Options = require "./options"
    App.Router = new Router()
    Backbone.history.start()

module.exports = startApp
