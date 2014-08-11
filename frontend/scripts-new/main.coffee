$ = require("jquery")
console.log "Grabbing App"
App = require("./app")
console.log "App grabbed"

Spine = require("spine")
Spine.$ = $
require("spine/lib/route")


startApp = (data)->
    $(".loading").remove()
    window.App = new App(data)
    console.log "Starting App"
    Spine.Route.setup()

console.log "Starting to get data"

$("body").append "<img class='loading' src='/images/ajax-loader.gif' />"

$.ajax
    url: "/data/data.json"
    dataType:"json",
    success: startApp,
    error: (request, textStatus, errorThrown) ->
        console.log(textStatus)
        console.log(errorThrown)
