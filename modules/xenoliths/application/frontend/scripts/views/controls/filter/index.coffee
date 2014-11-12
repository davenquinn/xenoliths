$ = require("jquery")
TagFilter = require("../tag-filter")
Spine = require "spine"
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

class FilterData extends Spine.Controller
  constructor: ->
    super
    @map = @parent.map
    @samples = App.Options.samples
    @render()

  events:
    "change #filter-settings input": "toggleControls"
    "click  button.filter": "filterData"

  render: ->
    a = this
    @$el.html template
      samples: App.Options.samples
      minerals: App.Options.minerals

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
        duration: 500


  toggleControls: (event) ->
    checked = event.target.checked
    cls = event.target.name.split("-")[1]
    @$("." + cls).toggle checked,
      duration: 300

  filterData: (event) ->
    arr = @$("form").serializeObject()
    ["minerals","samples"].forEach (d) ->
      delete arr[d] unless arr["filter-" + d] is "on"
      delete arr["filter-" + d]

    arr["tags"] = @tagFilter.getFilter()  if arr["filter-tags"] is "on"
    console.log arr
    data = App.Data.filter(arr)
    @map.setData data
    return

module.exports = FilterData
