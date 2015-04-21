$ = require("jquery")
d3 = require("d3")
Spine = require "spine"

template = require("./template.html")
Options = require("../../options")

responseHandler = (cb)->
  (err,r)->
    if err?
      console.log err,r
    else
      console.log r.response
      cb r.response

class TagManager extends Spine.Controller
  constructor: ->
    super
    @tags = []
    @collection = []

    @el.html template
    @ul = d3.select("#tag_field")

  events:
    "click span.remove": "removeTag"
    "click button": "addTag"
    "keypress input[type=text]": "addTagOnEnter"

  bindData: (ul, tags) ->
    li = ul.selectAll "li"
      .data tags, (d) -> tags.indexOf d

    li.exit().remove()
    li.enter().append("li")
      .html (d) -> d.name
      .attr "class", (d) ->
        if d.all then "all" else "some"
      .append "span"
        .html "<i class='fa fa-times'></i>"
        .attr "class", "remove"

  update: (data) ->
    @tags = @processData(data)
    @ul.call @bindData, @tags

  processData: (data) ->

    #takes a list of point items and outputs an object containing
    # tags as indices to boolean values for whether the tag is shared
    # by all items.
    if typeof (data) is "undefined"
      @tags.length = 0
      return @tags
    @collection = data
    nitems = data.length
    arrays = data.map (d) -> d.properties.tags
    arr = [].concat.apply([], arrays)

    rfunc = (acc, curr) ->
      acc[curr] = 0 if not acc[curr]?
      acc[curr] += 1
      return acc
    ndata = arr.reduce rfunc, {}

    @tags.length = 0
    for i of ndata
      @tags.push
        name: i
        all: (if ndata[i] >= data.length then true else false)
    @tags

  removeTag: (event) ->
    event.preventDefault()
    data = event.currentTarget.parentNode.__data__
    tag = data.name

    data =
      tag: tag
      points: @collection.map (d)->d.id

    cb = responseHandler (r)=>
      index = @tags.indexOf(data)
      @tags.splice index, 1

      for d in @collection
        tags = d.properties.tags
        i = tags.indexOf r.tag
        tags.splice i,1 unless i == -1

      @ul.call @bindData, @tags

    App.api "/point/tag"
      .send "DELETE", JSON.stringify(data), cb

  addTagOnEnter: (e) ->
    @addTag(e) if e.keyCode is 13

  addTag: (event) ->
    event.preventDefault()
    arr = @$("form").serializeObject()
    @$("input[type=text]").val ""
    return false  if arr.tag is ""
    tag = arr.tag.toLowerCase()
    data =
      tag: tag
      points: @collection.map (d)->d.id

    cb = responseHandler (r)=>
      for d in @collection
        tags = d.properties.tags
        tags.push tag if tags.indexOf(tag) is -1

      @ul.call @bindData, @processData(@collection)
      App.Data.Measurement.updateTags [tag]

    App.api "/point/tag"
      .send "POST", JSON.stringify(data), cb


module.exports = TagManager
