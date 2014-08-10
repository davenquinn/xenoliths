var chart_options = require('../chart/chart-options');
var map_options = require('./map-options');
var classify_options = require('./classify-options');
var data_frame = require('./data');
var raw_data = require('./raw-data');
var filter = require('./filter');


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
module.exports = Controls;

