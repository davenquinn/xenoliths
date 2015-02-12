Spine = require "spine"
template = require "./template.html"

class IndexPage extends Spine.Controller
  constructor: ->
    super
    @el.html template

module.exports = IndexPage
