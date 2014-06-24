$ = require("jquery")
console.log "Grabbing App"
App = require("./app")
console.log "App grabbed"

startApp = (data)->
    Route = require("spine-route").Route
    $(".loading").remove()
    window.App = new App(data)
    console.log "Starting App"
    Route.setup()

console.log "Starting to get data"

$("body").append "<img class='loading' src='/images/ajax-loader.gif' />"

$.ajax
    url: "/data.json"
    dataType:"json",
    success: startApp,
    error: (request, textStatus, errorThrown) ->
        console.log(textStatus)
        console.log(errorThrown)
