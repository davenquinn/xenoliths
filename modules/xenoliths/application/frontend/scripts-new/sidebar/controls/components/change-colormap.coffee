Spacepen = require "space-pen"
Options = require "../../../options"

class ChangeColormap extends Spacepen.View
    @content: ->
        @div =>
            @label "Colormap", for: "colormap"
            @select name: "colormap", class: "form-control", =>
                @option "Oxide Totals", value: "oxide_total", selected: true
                @option "Minerals", value: "minerals"
                @option "Samples", value: "samples"
                for oxide in Options.oxides
                    @option oxide, value: oxide

    events:
        "change select[name=colormap]": "changeColormap"

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

module.exports = ChangeColormap
