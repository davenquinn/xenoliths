d3 = require "d3"
Spacepen = require "space-pen"

class Controls extends Spacepen.View
    @content: =>
        @div class: "controls", =>
            @a "Select All", outlet: "all"
            @a "Select None", outlet: "none"
            @a "Exclude Bad", outlet: "exclude"

class TagFilter extends Spacepen.View
    @content: (options)->
        @div =>
            @ul id: "tag-filterlist"
            @subview "controls", new Controls

    initialize: ->
        @tags = App.Data.getTags()
        @ul = d3.select("#tag-filterlist")
        @ul.call @bindData, @prepareData()

    events:
        "click li": "changeTag"
        "click a": "selectData"

    prepareData: ->
        @data = @tags.map((item) ->
            name: item
            sel: true
        )
        @data

    selectData: (event) ->
        v = event.target.href.split("#")[1]
        if v is "all"
            @data.forEach (d) ->
                d.sel = true
                return

        else if v is "none"
            @data.forEach (d) ->
                d.sel = null
                return

        else if v is "bad"
            @data.forEach (d) ->
                d.sel = false    if App.Options.bad_tags.indexOf(d.name) > -1
                return

        @ul.call @bindData, @data
        false

    bindData: (ul, data) ->
        li = ul.selectAll("li").data(data, (d) ->
            d.name
        )
        li.enter().append("li").html (d) ->
            d.name

        li.attr "class", (d) ->
            unless d.sel?
                "ignore"
            else
                (if d.sel then "include" else "exclude")

        return

    getFilter: ->
        reduce = (d) ->
            d.name

        include: @data.filter((d) ->
            d.sel
        ).map(reduce)
        exclude: @data.filter((d) ->
            d.sel is false
        ).map(reduce)

    changeTag: (event) ->
        d = event.currentTarget.__data__

        #var d = this.data[this.data.indexOf(data)];
        unless d.sel?
            d.sel = false
        else
            d.sel = (if d.sel then null else true)
        @ul.call @bindData, @data
        return

module.exports = TagFilter
