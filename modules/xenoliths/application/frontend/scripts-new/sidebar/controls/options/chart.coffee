Spacepen = require("space-pen")
Options = require("../../../options")

class OptionsView extends Spacepen.View
    @content: ->
        @div =>
            @form =>
                @fieldset =>
                    @legend "Axes"
                    @div class: "form-group", =>
                        @label "X Axis", for: "x-axis"
                        @input
                            type:"text"
                            class:"form-control"
                            id:"x-axis"
                            value:"oxides.MgO"
                    @div class: "form-group", =>
                        @label "Y Axis", for: "y-axis"
                        @input
                            type:"text"
                            class:"form-control"
                            id:"y-axis"
                            value:"oxides.FeO"
                    @button "Change Axes",
                        type: "button"
                        class: "axes btn btn-default"
                @fieldset id: "colormap", =>
                    @label "Colormap", for: "colormap"
                    @select name:"colormap", class: "form-control", =>
                        @option "Oxide Totals", value: "oxide_total", selected: true
                        @option "Minerals", value: "minerals"
                        @option "Samples", value: "samples"
                        for oxide in Options.oxides
                            @option oxide, value: oxide
    initialize: ->
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

module.exports = OptionsView
