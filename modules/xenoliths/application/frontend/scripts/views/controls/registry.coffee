chart_options = require("../chart/chart-options")
map_options = require("./map-options")
raw_data = require("./raw-data")
filter = require("./filter")
Controls =
  raw:
    name: "Raw"
    obj: raw_data

  "chart-options":
    name: "Options"
    obj: chart_options

  "map-options":
    name: "Options"
    obj: map_options

  data:
    name: "Data"
    obj: require "../../controls/chart-panel"

  filter:
    name: "Filter"
    obj: filter

module.exports = Controls
