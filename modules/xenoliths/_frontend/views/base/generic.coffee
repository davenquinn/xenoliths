Backbone = require("backbone")
Handlebars = require("handlebars")
GenericView = Backbone.View.extend(
  initialize: (options) ->
    @options = options
    console.log options
    @parent = @options.parent
    @map = @parent.map
    return

  assign: (view, selector) ->
    
    #http://ianstormtaylor.com/rendering-views-in-backbonejs-isnt-always-simple/
    view.setElement(@$(selector)).render()
    return

  remove: ->
    
    # Empty the element and remove it from the DOM while preserving events
    $(@el).empty().detach()
    this

  compile: (template) ->
    @template = template
    @template

  destroy_view: ->
    
    #COMPLETELY UNBIND THE VIEW
    @undelegateEvents()
    @$el.removeData().unbind()
    
    #Remove view from DOM
    @remove()
    Backbone.View::remove.call this
    return
)
module.exports = GenericView
