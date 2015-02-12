d3 = require("d3")

Spine = require "spine"

class OxideTotal
  constructor: ->
    @values = d3.scale.sqrt().domain([0,10]).range ["#71eeb8","salmon"]
  func: (d) => @values 100-d.properties.oxides.Total

class Oxide
  constructor: (o)->
    @data = o.data
    @oxide = o.oxide
    @values = d3.scale.linear()
      .domain d3.extent @data.features,
        (d)=> d.properties.oxides[@oxide]
      .range ["#71eeb8","salmon"]

   func: (d) =>
      @values d.properties.oxides[@oxide]

class Sample
  func: (d) -> App.Options.samples[d.properties.sample].color

class Mineral
  func: (d) -> App.Options.minerals[d.properties.mineral].color


module.exports =
  oxide_total: OxideTotal
  oxide: Oxide
  samples: Sample
  minerals: Mineral
