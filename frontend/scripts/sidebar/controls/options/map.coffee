Spacepen = require "space-pen"
SelectMap = require "../components/select-map"
ChangeColormap = require "../components/change-colormap"

class MapOptions extends Spacepen.View
	@content: ->
		@div =>
			@subview "select-map", new SelectMap
			@subview "colormap", new ChangeColormap

module.exports = MapOptions
