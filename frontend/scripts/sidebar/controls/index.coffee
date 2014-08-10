module.exports =
    raw:
        name: "Raw"
        obj: require("./raw-data")

    data:
        name: "Data"
        obj: require("./data")

    "chart-options":
        name: "Options"
        obj: require("./options/chart")

    "map-options":
        name: "Options"
        obj: require("./options/map")

    filter:
        name: "Filter"
        obj: require("./filter")
