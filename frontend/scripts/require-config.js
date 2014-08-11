require.config({
    shim: {
        "openlayers": {
            exports: 'OpenLayers'
        },
        "jquery.bootstrap": {
            deps: ["jquery"]
        },
        "jquery.slider": {
            deps: ["jquery"]
        },
        "bootstrap-switch": {
            deps: ["jquery"]
        }
    },
    urlArgs: "bust=" +  (new Date()).getTime(),
    paths: {
        "classy": "lib/classy/classy",
        "jquery": null,
        "underscore": null,
        "backbone": null,
        "handlebars": null,
        "openlayers": "lib/openlayers/OpenLayers",
        "d3": null,
        "jquery.bootstrap": "lib/bootstrap/dist/js/bootstrap",
        "jquery.slider": "lib/jquery-simple-slider/js/simple-slider",
        "bootstrap-switch": "lib/bootstrap-switch/static/js/bootstrap-switch",
        "text" : "lib/requirejs-text/text",
    }
});
