$ = require "jquery"
TagFilter = require "./tags"
Spine = require "spine"
template = require "./filter.html"

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
    "click  button.filter": "filterData"

  render: ->
    a = this
    @$el.html template
      samples: App.Options.samples
      minerals: App.Options.minerals

    @tagFilter = new TagFilter
      el: @$("#tag-filter")
      parent: @

    sections = [
      "samples"
      "minerals"
      "tags"
    ]

    @sections = sections.map (d)->
      {name: d, enabled: false}

    @selection = d3.select @el[0]
      .selectAll ".form-group"
        .data @sections

    refresh = (sel)->
      sel.select "label i"
        .attr class: (d)->
          s = if d.enabled then "circle" else "circle-o"
          "fa fa-"+s
      sel.select ".panel"
        .each (d)->
          o = $ @
          if d.enabled
            o.show 500
          else
            o.hide 500

    @selection
      .call refresh
      .select "label"
        .on "click", (d)=>
          d.enabled = not d.enabled
          @selection.call refresh

  filterData: (event) =>
    form = @$("form").serializeObject()

    arr = {}
    for i in @selection.data()
      continue unless i.enabled
      if i.name is "tags"
        arr[i.name] = @tagFilter.getFilter()
      else
        arr[i.name] = form[i.name]

    console.log arr
    data = App.Data.filter(arr)
    @map.setData data
    event.preventDefault()
    false

module.exports = FilterData
