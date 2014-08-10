Spacepen = require("space-pen")
Controls = require("./controls")

class Sidebar extends Spacepen.View
    @content: (controls)->
        @div id: "sidebar", =>
            @div class: "navbar", =>
                @ul class: "nav navbar-nav", outlet: "list", =>
                    for control in controls
                        @li =>
                            @a Controls[control].name, href: control
            @div id: "tabs", =>
                for control in controls
                    @subview control, new Controls[control].obj

    initialize: (controls)->
        @activeTab = "#" + controls[0]
        @find(".navbar-nav a").on "click", @onNav

    render: ->
        controls = []
        for c of @options.controls
            id = @options.controls[c]
            control = Controls[id]
            control.id = id
            controls.push control
        opts = controls: controls
        @$el.html @template(opts)
        for c of controls
            control = controls[c]
            control = new control.obj(
                el: "#" + control.id
                parent: this
                map: @map
            )
        @viewTab @activeTab
        return

    refresh: ->
        for c of @controls
            @controls[c].remove()
        @render()
        return

    onNav: (event) =>
        event.preventDefault()
        val = event.currentTarget.hash
        @activeTab = val
        @viewTab val
        console.log val

    viewTab: (tab) ->
        @find(".navbar-nav li").removeClass "active"
        @find("#tabs>div").hide()
        @find("a[href=#{tab}]").parent().addClass "active"
        @find(tab).show()

module.exports = Sidebar
