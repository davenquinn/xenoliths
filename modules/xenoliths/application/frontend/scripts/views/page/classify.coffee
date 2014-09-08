GenericView = require("../base/generic")
MapPanel = require("../map/classify")
Options = require("../controls/classify-options")
SelectMap = require("../controls/select-map")
template = require("../../templates/page/classify.html")

ClassifyPage = GenericView.extend
    initialize: (options) ->
        @options = options
        @sample = @options.sample
        @sample = "CK-2" if @sample is null
        @compile template
        @setup()

    setup: ->
        App.API
            url: "/sample/classification/"+@sample
            type: 'GET'
            success: (data) =>
                @data = data.result
                console.log data
                @render()

    render: ->
        @$el.html @template
        @map = new MapPanel(
            el: "#map"
            parent: this
            sample: @sample
        )
        @sel = new SelectMap(
            el: "#select_map"
            parent: this
        )
        @opt = new Options(
            el: "#options"
            parent: this
        )
        @sel.setSelected @sample

    onSampleChanged: (sample) ->
        @sample = sample
        @map.remove()
        @sel.remove()
        @opt.remove()
        @setup()

    onSaved: ->
        App.JSON_RPC "save_classification",
            sample: @sample
            classification: @map.getData()
        , (data, err) ->
            self.data = data.result
            console.log data
            return

module.exports = ClassifyPage
