$ = require "jquery"
d3 = require "d3"
Spine = require "spine"
template = require "./template.html"

class TagFilter extends Spine.Controller
  constructor: ->
    super
    @tags = App.Data.getTags()

    @el.html template
    @ul = d3.select("#tag-filterlist")
    @ul.call @bindData, @prepareData()

  events:
    "click li": "changeTag"
    "click a": "selectData"

  prepareData: ->
    @data = @tags.map((item) ->
      name: item
      sel: true
    )
    @data

  selectData: (event) ->
    v = event.target.href.split("#")[1]
    if v is "all"
      @data.forEach (d) ->
        d.sel = true
        return

    else if v is "none"
      @data.forEach (d) ->
        d.sel = null
        return

    else if v is "bad"
      @data.forEach (d) ->
        d.sel = false  if App.Options.bad_tags.indexOf(d.name) > -1
        return

    @ul.call @bindData, @data
    false

  bindData: (ul, data) ->
    li = ul.selectAll("li").data(data, (d) ->
      d.name
    )
    li.enter().append("li").html (d) ->
      d.name

    li.attr "class", (d) ->
      unless d.sel?
        "ignore"
      else
        (if d.sel then "include" else "exclude")

    return

  getFilter: ->
    reduce = (d) ->
      d.name

    include: @data.filter((d) ->
      d.sel
    ).map(reduce)
    exclude: @data.filter((d) ->
      d.sel is false
    ).map(reduce)

  changeTag: (event) ->
    d = event.currentTarget.__data__
    
    #var d = this.data[this.data.indexOf(data)];
    unless d.sel?
      d.sel = false
    else
      d.sel = (if d.sel then null else true)
    @ul.call @bindData, @data
    return
)
module.exports = TagFilter
