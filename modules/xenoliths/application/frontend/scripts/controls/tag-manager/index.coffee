$ = require("jquery")
d3 = require("d3")
GenericView = require("../../views/base/generic")

template = require("./template.html")
Options = require("../../options")

TagManager = GenericView.extend(
  initialize: ->
    @compile template
    @tags = []
    @data = []
    @render()
    return

  render: ->
    @$el.html @template
    @ul = d3.select("#tag_field")

    #this.ul.call(this.bindData,[])
    this

  events:
    "click .icon-remove": "removeTag"
    "click button": "addTag"
    "keypress input[type=text]": "addTagOnEnter"

  bindData: (ul, tags) ->
    li = ul.selectAll("li").data(tags, (d) ->
      tags.indexOf d
    )
    li.exit().remove()
    li.enter().append("li").html((d) ->
      d.name
    ).attr("class", (d) ->
      (if d.all then "all" else "some")
    ).append("span").html("<i class='icon-remove'></i>").attr "class", "remove"
    return

  update: (data) ->
    @tags = @processData(data)
    @ul.call @bindData, @tags
    return

  processData: (data) ->

    #takes a list of point items and outputs an object containing
    # tags as indices to boolean values for whether the tag is shared
    # by all items.
    if typeof (data) is "undefined"
      @tags.length = 0
      return @tags
    @data = data
    nitems = data.length
    arrays = data.map((item) ->
      item.properties.tags
    )
    arr = [].concat.apply([], arrays)
    ndata = arr.reduce((acc, curr) ->
      if typeof acc[curr] is "undefined"
        acc[curr] = 1
      else
        acc[curr] += 1
      acc
    , {})
    @tags.length = 0
    for i of ndata
      obj =
        name: i
        all: (if ndata[i] >= data.length then true else false)

      @tags.push obj
    @tags

  removeTag: (event) ->
    data = event.currentTarget.parentNode.__data__
    tag = data.name
    index = @tags.indexOf(data)
    elements = []
    @tags.splice index, 1
    for i of @data
      d = @data[i]
      tags = d.properties.tags
      ind = tags.indexOf(tag)
      tags.splice ind, 1  unless ind is -1
      elements.push [
        d.properties.sample
        d.properties.id
      ]
    App.JSON_RPC "remove_tag",
      tag: tag
      points: elements

    @ul.call @bindData, @processData(@data)
    return

  addTagOnEnter: (e) ->
    return  unless e.keyCode is 13
    @addTag()
    false

  addTag: (event) ->
    arr = @$("form").serializeObject()
    @$("input[type=text]").val ""
    return false  if arr.tag is ""
    tag = arr.tag.toLowerCase()
    elements = []
    for i of @data
      d = @data[i]
      tags = d.properties.tags
      tags.push tag  if tags.indexOf(tag) is -1
      elements.push [
        d.properties.sample
        d.properties.id
      ]
    App.JSON_RPC "add_tag",
      tag: tag
      points: elements

    @ul.call @bindData, @processData(@data)
    App.Data.pushTag tag
    false
)
module.exports = TagManager
