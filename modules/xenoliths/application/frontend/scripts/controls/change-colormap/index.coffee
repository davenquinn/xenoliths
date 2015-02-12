$ = require("jquery")
GenericView = require("../../views/base/generic")
Options = require("../../options")
template = require "./template.html"

ChangeColormap = GenericView.extend(
  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    @compile template
    @render()
    return

  events:
    "change select[name=colormap]": "changeColormap"

  render: ->
    @$el.html @template(oxides: Options.oxides)
    this

  changeColormap: (event) ->
    val = $(event.currentTarget).val()
    if Options.oxides.indexOf(val) > -1
      console.log val
      @map.setColormap "oxide",
        oxide: val
        data: @map.data

    else
      @map.setColormap val
    return
)
module.exports = ChangeColormap
