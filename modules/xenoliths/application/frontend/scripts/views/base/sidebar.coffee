$ = require("jquery")
GenericView = require("./generic")
template = require("../../templates/base/sidebar.html")
Controls = require("../controls/registry")
Sidebar = GenericView.extend(
  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    @activeTab = "#" + @options.controls[0]
    @compile template
    @render()
    return

  render: ->
    controls = []
    for c of @options.controls
      id = @options.controls[c]
      control = Controls[id]
      control.id = id
      controls.push control
    opts = controls: controls
    @$el.html @template(opts)
    for c of controls
      control = controls[c]
      control = new control.obj(
        el: "#" + control.id
        parent: this
        map: @map
      )
    @viewTab @activeTab
    return

  refresh: ->
    for c of @controls
      @controls[c].remove()
    @render()
    return

  events:
    "click .navbar-nav a": "onNav"

  onNav: (event) ->
    val = event.currentTarget.hash
    @activeTab = val
    @viewTab val
    false

  viewTab: (tab) ->
    @$(".navbar-nav li").removeClass "active"
    @$("#tabs>div").hide()
    @$("a[href=" + tab + "]").parent().addClass "active"
    $(tab).show()
    return
)
module.exports = Sidebar
