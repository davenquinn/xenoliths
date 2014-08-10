$ = require "jquery"
Spine = require("spine")
Data = require "./data"

class App
    constructor: (data) ->
        @Options = require "../options"
        routes = require "./routes"
        @Data = new Data(data)
        for own url, func of routes
            Spine.Route.add url, func
        console.log "Finished setting up routes"
    State:
        page: null
        viewer: null

module.exports = App
