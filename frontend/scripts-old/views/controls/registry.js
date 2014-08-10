define([
    "views/chart/chart-options",
    "views/controls/map-options",
    "views/controls/classify-options",
    "views/controls/data",
    "views/controls/raw-data",
    "views/controls/filter"
    ],function(chart_options, map_options, classify_options, data_frame, raw_data, filter){

    var Controls = {
        "raw": {
            "name": "Raw",
            "obj": raw_data
        },
        "data": {
            "name": "Data",
            "obj": data_frame
        },
        "chart-options": {
            "name": "Options",
            "obj": chart_options
        },
        "map-options": {
            "name": "Options",
            "obj": map_options
        },
        "filter": {
            "name": "Filter",
            "obj": filter
        },
    };
    return Controls;
});
