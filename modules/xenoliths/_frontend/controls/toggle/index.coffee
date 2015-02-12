Spine = require "spine"
Dragdealer = require("dragdealer").Dragdealer

int = (v) -> if v then 1 else 0

class Toggle extends Spine.Controller
  className: "dragdealer"
  events:
    "click": "onClick"
  constructor: ->
    super
    @labels = ["Disabled","Enabled"] unless @labels
    @values = [false,true] unless @values
    @$el.append "<div class='handle red-bar'></div>"
    @handle = @$(".handle")
    @enabled = false unless @enabled
    @handle.text @labels[int(@enabled)]
    @slider = new Dragdealer @el[0],
      x: int @enabled
      steps: 2
      callback: (x)=>
        return if int(@enabled) == x
        @enabled = if x == 1 then true else false
        @handle.text @labels[x]
        @trigger "change", @values[int(@enabled)]

  onClick: ->
    @change()

  change: ->
    @slider.setValue int(not @enabled)

  value: => @values[int(@enabled)]

module.exports = Toggle
