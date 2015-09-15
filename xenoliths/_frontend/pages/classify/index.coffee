SelectMap = require("../../controls/map/select")
MapPanel = require("./map")
Options = require("./options")
template = require("./template.html")
Spine = require "spine"

class ClassifyPage extends Spine.Controller
    constructor: ->
        super
        @sample = "CK-2" if @sample is null
        @setup()

    setup: ->
        App.API
            url: "/sample/classification/#{@sample}"
            type: 'GET'
            success: (@data) => @render()

    render: ->
        @$el.html template
        @map = new MapPanel
            el: "#map"
            parent: @
            sample: @sample

        @sel = new SelectMap
            el: "#select_map"
            parent: this

        @opt = new Options el: "#options"
        @opt
          .bind "change:opacity", (d)=> @map.setOpacity d
          .bind "change:mineral", (d)=> @map.setMineral d
          .bind "change:draw-enabled", (d)=> @map.setDraw d
          .bind "save", => @onSaved()

        @map.setOpacity @opt.defaults.opacity
        @sel.setSelected @sample

    onSampleChanged: (sample) ->
        @sample = sample
        @map.el.remove()
        @sel.el.remove()
        @opt.el.remove()
        @setup()

    onSaved: ->
      data = @map.getData()
      console.log data
      App.API
        url: "/sample/classification/#{@sample}"
        type: "POST"
        data: data
        success: (d) -> console.log d

module.exports = ClassifyPage
