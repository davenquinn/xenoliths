Spine = require "spine"

class Selection extends Spine.Module
  @extend Spine.Events
  collection: []
  add: (d)=>
    return if @contains d
    @collection.push d
    @constructor.trigger "add", d
  remove: (d)=>
    i = @collection.indexOf d
    return if i == -1
    @collection.splice i,1
    @constructor.trigger "remove", d
  empty: =>
    @collection = []
    @constructor.trigger "empty"
  contains: (d)=>
    @collection.indexOf(d) >= 0

module.exports = Selection
