$ = require("jquery")
GenericView = require("../base/generic")
OxidesWheel = require("./oxides")
MultiSelect = require("./multi-select")
TagManager = require("./tag-manager")
template = require("../../templates/controls/data-frame.html")
Options = require("../../options")
require "bootstrap-switch"
DataFrame = GenericView.extend(
  initialize: (options) ->
    @options = options
    a = this
    @map = @options.map
    @compile template
    @render()
    @oxides = new OxidesWheel(
      el: "#oxides"
      parent: this
    )
    @tags = new TagManager(
      el: "#tag_manager"
      parent: this
    )
    @multiSelect = new MultiSelect(
      el: "#multiple"
      parent: this
    )
    @tdata = null
    if @map.sel
      @update @map.sel[0]
    else
      @update @map.data.features[0]
    @map.dispatcher.on "updated.data", (d) ->
      sel = d3.select(this)
      a.tdata = d  if sel.classed("selected")
      a.update d
      return

    @map.dispatcher.on "mouseout", (d) ->
      sel = d3.select(this)
      a.update null
      return

    return

  render: ->
    @$el.html @template
    this

  update: (data) ->
    unless data?
      @tags.update @map.sel
      data = @tdata
    else
      @tags.update [data]
    @multiSelect.update @map.sel
    return  unless data?
    id = data.properties.id
    sample = data.properties.sample
    @$(".id").html id
    @$(".sample").html sample
    @$(".map-link").attr "href", "#map/" + sample + "/point/" + id
    @oxides.update data
    return
)
module.exports = DataFrame
