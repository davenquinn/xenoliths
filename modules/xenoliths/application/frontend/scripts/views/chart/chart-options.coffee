$ = require("jquery")
GenericView = require("../base/generic")
Options = require("../../options")
template = require("../../templates/chart/chart-options.html")
OptionsView = GenericView.extend(
  initialize: (options) ->
    @options = options
    @parent = @options.parent
    @map = @parent.map
    @compile template
    @render()
    return

  events:
    "change select[name=colormap]": "changeColormap"
    "click  button.axes": "changeAxes"

  render: ->
    @$el.html @template(oxides: Options.oxides)
    this

  changeColormap: (event) ->
    val = $(event.currentTarget).val()
    if Options.oxides.indexOf(val) > -1
      @map.setColormap "oxide",
        oxide: val
        data: @map.data

    else
      @map.setColormap val
    return

  changeAxes: (event) ->
    axes =
      x: @$("#x-axis").val()
      y: @$("#y-axis").val()

    @map.setAxes axes
    false
)
module.exports = OptionsView
