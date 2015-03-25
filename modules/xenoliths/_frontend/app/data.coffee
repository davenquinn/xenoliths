Spine = require "spine"

inArr = (arr)->
  (t) -> arr.indexOf(t) > -1
notIn = (arr)->
  (t) -> arr.indexOf(t) == -1

class Measurement extends Spine.Module
  @extend Spine.Events
  @collection: []
  @tags: []
  @index: new Array
  @get: (id)->@index[id]
  @updateTags: (tags)->
    newTags = tags.filter notIn(@tags)
    for t in newTags
      @tags.push t

  @hovered: (d)->
    d.hovered = not d.hovered
    @trigger "hovered", d

  constructor: (obj)->
    super
    for key of obj
      @[key] = obj[key]
    @constructor.collection.push @
    @constructor.index[@id] = @
    @constructor.updateTags @properties.tags

class Data
  constructor: (@data) ->
    for f in @data.features
      new Measurement(f)

    @data.features = Measurement.collection
    @tags = Measurement.tags

  getTags: => @tags

  pushTag: (tag) ->
    if Measurement.tags.indexOf(tag) is -1
      Measurement.tags.push tag

  filter: (options) ->

    for item in ["samples","minerals"]
      if typeof (options[item]) is "string"
        options[item] = [options[item]]

    tests = {}
    if options.samples?
      tests.samples = notIn options.samples
    if options.minerals?
      tests.minerals = notIn options.minerals
    if options.tags?
      tests.tags =
        excluded: inArr options.tags.exclude
        included: inArr options.tags.include

    test = (d)->
      if tests.samples?
        return false if tests.samples(d.properties.sample)
      if tests.minerals?
        return false if tests.minerals(d.properties.mineral)
      if tests.tags?
        if d.properties.tags.some(tests.tags.excluded)
          return false
        else if d.properties.tags.some(tests.tags.included)
          return true
        else
          return false
      return true

    arr = Measurement.collection.filter test
    out =
      type: "FeatureCollection"
      features: arr

module.exports = Data
