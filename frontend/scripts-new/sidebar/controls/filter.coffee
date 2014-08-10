$ = require "jquery"
Spacepen = require "space-pen"
TagFilter = require "./components/tag-filter"

$.fn.serializeObject = ->
	o = {}
	a = @serializeArray()
	$.each a, ->
		if o[@name]
			o[@name] = [o[@name]]	unless o[@name].push
			o[@name].push @value or ""
		else
			o[@name] = @value or ""
		return

	o

class Checkbox extends Spacepen.View
	@content: (label, name)->
		@label class: "checkbox-inline", =>
			@input type: "checkbox", name: name
			@text label

class Select extends Spacepen.View
	@content: (options) ->
		options.multiple ? false
		@div class: "form-group #{options.name}", =>
			@label options.label, for: options.name
			@select
				multiple: options.multiple
				name: options.name
				class: "form-control"
				=>
					for choice in options.choices
						@option choice, value: choice


class FilterData extends Spacepen.View
	@content: (options) ->
		@form =>
			@fieldset =>
				@legend "Filter Data"
				@div class:"form-group", id:"filter-settings", =>
					for type in ["samples", "minerals", "tags"]
						@subview "filter_#{type}", new Checkbox("filter-#{type}", "Filter #{type}")
				@subview "samples", new Select
					multiple: true
					name: "samples"
					label: "Sample"
					choices: window.App.Options.samples
				@subview "samples", new Select
					multiple: true
					name: "mineral"
					label: "Mineral"
					choices: window.App.Options.minerals
				@div class: "form-group tags", =>
					@label "Tags"
					@subview "tag_filter", new TagFilter
				@button "Filter", type: "button", class: "filter btn btn-default"

	events:
		"change #filter-settings input": "toggleControls"
		"click  button.filter": "filterData"

	render: ->
		a = this
		@$el.html @template(
			samples: @samples
			minerals: window.App.Options.minerals
		)
		@tagFilter = new TagFilter(
			el: @$("#tag-filter")
			parent: this
		)
		$.each [
			"minerals"
			"samples"
			"tags"
		], (i, d) ->
			condition = a.$("input[name=filter-" + d + "]").is(":checked")
			a.$("div." + d).toggle condition,
				duration: 300

			return

		this

	toggleControls: (event) ->
		checked = event.target.checked
		cls = event.target.name.split("-")[1]
		console.log cls
		@$("." + cls).toggle checked,
			duration: 300

		return

	filterData: (event) ->
		arr = @$("form").serializeObject()
		$.each [
			"minerals"
			"samples"
		], (i, d) ->
			delete arr[d]	unless arr["filter-" + d] is "on"
			delete arr["filter-" + d]

			return

		arr["tags"] = @tagFilter.getFilter()	if arr["filter-tags"] is "on"
		console.log arr
		data = window.App.Data.filter(arr)
		@map.setData data
		return

module.exports = FilterData
