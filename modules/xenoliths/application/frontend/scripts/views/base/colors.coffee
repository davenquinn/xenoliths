$ = require("jquery")
Class = require("./classy")
d3 = require("d3")
Options = require("../../options")
ColorMap = Class.$extend({})
ColorMaps =
  oxide_total: ColorMap.$extend(__init__: (options) ->
    a = this
    @values = d3.scale.sqrt().domain([
      0
      10
    ]).range([
      "#71eeb8"
      "salmon"
    ])
    @func = (d) ->
      a.values 100 - d.properties.oxides.Total

    return
  )
  oxide: ColorMap.$extend(__init__: (options) ->
    a = this
    @oxide = options.oxide
    @data = options.data
    @domain = d3.extent(@data.features, (d) ->
      d.properties.oxides[a.oxide]
    )
    @values = d3.scale.linear().domain(@domain).range([
      "#71eeb8"
      "salmon"
    ])
    @func = (d) ->
      a.values d.properties.oxides[a.oxide]

    return
  )
  samples: ColorMap.$extend(__init__: (options) ->
    a = this
    @values = Options.samples
    @func = (d) ->
      a.values[d.properties.sample].color

    return
  )
  minerals: ColorMap.$extend(__init__: (options) ->
    a = this
    @values = Options.minerals
    @func = (d) ->
      a.values[d.properties.mineral].color

    return
  )

module.exports = ColorMaps
