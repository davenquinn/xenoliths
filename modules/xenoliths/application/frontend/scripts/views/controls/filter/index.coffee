$ = require("jquery")
GenericView = require("../../base/generic")
Options = require("../../../options")
App = require("../../../app")
TagFilter = require("../tag-filter")
template = require("./filter.html")
$.fn.serializeObject = ->
  o = {}
  a = @serializeArray()
  $.each a, ->
    if o[@name]
      o[@name] = [o[@name]]  unless o[@name].push
      o[@name].push @value or ""
    else
      o[@name] = @value or ""
    return

  o

FilterData = GenericView.extend(
  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    
    #if (this.sample === typeof("undefined")) {
    #            this.show_samples = true;
    #        } else this.show_samples = false;
    @samples = Options["samples"]
    @compile template
    @render()
    return

  events:
    "change #filter-settings input": "toggleControls"
    "click  button.filter": "filterData"

  render: ->
    a = this
    @$el.html @template(
      samples: @samples
      minerals: Options.minerals
    )
    @tagFilter = new TagFilter(
      el: @$("#tag-filter")
      parent: this
    )
    $.each [
      "minerals"
      "samples"
      "tags"
    ], (i, d) ->
      condition = a.$("input[name=filter-" + d + "]").is(":checked")
      a.$("div." + d).toggle condition,
        duration: 300

      return

    this

  toggleControls: (event) ->
    checked = event.target.checked
    cls = event.target.name.split("-")[1]
    console.log cls
    @$("." + cls).toggle checked,
      duration: 300

    return

  filterData: (event) ->
    arr = @$("form").serializeObject()
    $.each [
      "minerals"
      "samples"
    ], (i, d) ->
      delete arr[d]  unless arr["filter-" + d] is "on"
      delete arr["filter-" + d]

      return

    arr["tags"] = @tagFilter.getFilter()  if arr["filter-tags"] is "on"
    console.log arr
    data = window.App.Data.filter(arr)
    @map.setData data
    return
)
module.exports = FilterData
