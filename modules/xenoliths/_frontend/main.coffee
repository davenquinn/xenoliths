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

  console.log "Navigating"
  Spine.Route.setup()

console.log "Starting to get data"
$("body").append "<img class='loading' src='/static/images/ajax-loader.gif' />"
$.ajax
    url: "/data/data.json?bust=" + (new Date()).getTime()
    dataType: "json"
    success: startApp
    error: (request, textStatus, errorThrown) ->
        console.log textStatus
        console.log errorThrown
