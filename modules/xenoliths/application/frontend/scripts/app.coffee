$ = require("jquery")
Backbone = require("backbone")
Router = require("./router")
Data = require("./data")

App =
    JSON_RPC: (method, params, callback) ->
        url = "/json/"
        request =
            method: method
            params: params
            jsonrpc: "2.0"
            id: 1

        req = JSON.stringify(request)
        $.post url, req, callback, "json"
    API: (o)->
        o.url = "/api"+o.url
        return $.ajax(o)

startApp = (data) ->
    window.App = App
    App["Data"] = new Data(data)
    App["Router"] = new Router()
    Backbone.history.start()
    return

module.exports = startApp
