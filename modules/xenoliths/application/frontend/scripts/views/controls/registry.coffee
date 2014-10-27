chart_options = require("../chart/chart-options")
map_options = require("./map-options")
data_frame = require("./data")
raw_data = require("./raw-data")
filter = require("./filter")
Controls =
  raw:
    name: "Raw"
    obj: raw_data

  data:
    name: "Data"
    obj: data_frame

  "chart-options":
    name: "Options"
    obj: chart_options

  "map-options":
    name: "Options"
    obj: map_options

  filter:
    name: "Filter"
    obj: filter

module.exports = Controls
