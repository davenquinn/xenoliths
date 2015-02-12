Spine = require "spine"

class RawViewer extends Spine.Controller
  constructor: ->
    super
    @map.dispatcher.on "updated.raw", (d) =>
      @update d

    if @map.selected
      @update @map.selected
    else
      @update @map.data.features[0]

  syntaxHighlight: (json) ->
    json = JSON.stringify(json, "undefined", 2)  unless typeof json is "string"
    json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    json.replace /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, (match) ->
      cls = "number"
      if /^"/.test(match)
        if /:$/.test(match)
          cls = "key"
        else
          cls = "string"
      else if /true|false/.test(match)
        cls = "boolean"
      else cls = "null"  if /null/.test(match)
      "<span class=\"" + cls + "\">" + match + "</span>"


  update: (data) ->
    return  if typeof (data) is "undefined"
    @el.html "<pre>" + @syntaxHighlight(data) + "</pre>"

module.exports = RawViewer
