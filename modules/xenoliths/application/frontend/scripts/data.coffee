class Data
    constructor: (@data) ->
        @tags = []

    getTags: =>
        return @tags    if @tags.length > 0
        for d in @data.features
            for t in d.properties.tags
                @pushTag t

        @tags

    pushTag: (tag) ->
        if @tags.indexOf(tag) is -1
            @tags.push tag

    filter: (options) ->
        data = @data
        for item in ["samples","minerals"]
            options[item] = [options[item]] if typeof (options[item]) is "string"

        arr = @data.features
        if options.samples
            arr = arr.filter (d) ->
              options.samples.indexOf(d.properties.sample) > -1
        if options.minerals
            arr = arr.filter (d) ->
              options.minerals.indexOf(d.properties.mineral) > -1

        if options.tags
            excluded = (t) ->
                options.tags.exclude.indexOf(t) > -1

            included = (t) ->
                options.tags.include.indexOf(t) > -1

            arr = arr.filter (d) ->
                if d.properties.tags.some(excluded)
                    false
                else if d.properties.tags.some(included)
                    true
                else
                    false

        out =
            type: "FeatureCollection"
            features: arr

module.exports = Data
