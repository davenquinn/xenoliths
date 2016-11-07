$ = require "jquery"
window.jQuery = $
window.$ = $
Spine = require "spine"
Spine.jQuery = $
require "spine/lib/route"

App = require "./app"

startApp = (d)->
  new App
    el: "body"
    data: d

  Spine.Route.setup()

console.log "Starting to get data"
$("body").append "<img class='loading' src='/static/images/ajax-loader.gif' />"
$.ajax
    url: "/api/probe-data"
    dataType: "json"
    success: startApp
    error: (request, textStatus, errorThrown) ->
        console.log textStatus
        console.log errorThrown
