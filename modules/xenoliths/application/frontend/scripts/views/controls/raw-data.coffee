$ = require("jquery")
GenericView = require("../base/generic")
template = require("../../templates/controls/raw-data.html")
RawViewer = GenericView.extend(
  initialize: (options) ->
    @options = options
    a = this
    @parent = @options.parent
    @map = @options.map
    @compile template
    @map.dispatcher.on "updated.raw", (d) ->
      a.update d
      return

    if @map.selected
      @update @map.selected
    else
      @update @map.data.features[0]
    return

  events:
    "click button.close": "destroy"

  syntaxHighlight: (json) ->
    json = JSON.stringify(json, `undefined`, 2)  unless typeof json is "string"
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
    @$el.html "<pre>" + @syntaxHighlight(data) + "</pre>"
    return
)
module.exports = RawViewer
