Spacepen = require "space-pen"
Options = require "../../../options"

class SelectMap extends Spacepen.View
	@content: ->
		@div =>
			@label "Sample", for: "sample"
			@select name:"sample", class: "form-control", =>
				for key, value of Options.samples
					@option key, value: key
			@div class: "layer-switch", =>
				@input
					type:"checkbox"
					name:"layer-switch"
					class:"layer-switch-checkbox"
					id: "layer-switch"
					checked: true
				@label class: "layer-switch-label",for:"layer-switch", =>
					@div class: "layer-switch-inner"
					@div class: "layer-switch-switch"

	initialize: ->
		@samples = Options["samples"]
		@currentLayer = "sem"

	events:
		"change select[name=sample]": "sampleChanged"
		"change .layer-switch": "changeLayer"

	sampleChanged: (event) ->
		smp = $(event.currentTarget).val()
		@map.parent.onSampleChanged smp
		return

	setSelected: (sample) ->
		@$("select[name=sample]").val sample
		return

	changeLayer: (event) ->
		val = $(event.currentTarget).val()
		lyr = (if @currentLayer is "sem" then "scan" else "sem")
		@map.setLayer lyr
		@currentLayer = lyr
		return

module.exports = SelectMap
