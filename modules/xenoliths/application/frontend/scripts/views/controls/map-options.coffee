GenericView = require("../base/generic")
Controls = require("./registry")
SelectMap = require("./select-map")
ChangeColormap = require("./change-colormap")
MapOptions = GenericView.extend(
  initialize: (options) ->
    @options = options
    
    #this.__super__.initialize.apply(this,arguments)
    @parent = @options.parent
    @map = @parent.map
    @render()
    new SelectMap(
      el: "#select-map"
      parent: @parent
    )
    new ChangeColormap(
      el: "#colormap"
      parent: @parent
    )
    return

  render: ->
    @$el.html "<div id=\"select-map\"></div><div id=\"colormap\"></div>"
    this
)
module.exports = MapOptions
