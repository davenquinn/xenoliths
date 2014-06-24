({
    appDir: ".",
    baseUrl: "scripts",
    dir: "../frontend-build",
    modules: [
        {
            name: "main"
        }
    ],
    shim: {
         'handlebars': {
            exports: 'Handlebars'
        },
        "openlayers": {
            exports: 'OpenLayers'
        },
        "d3": {
            exports: 'd3'
        },
        "jquery.bootstrap": {
            deps: ["jquery"]
        },
        "jquery.slider": {
            deps: ["jquery"]
        },
        "jquery.switch": {
            deps: ["jquery"]
        }
    },
	paths: {
        "classy": "lib/classy/classy",
		"jquery": "lib/jquery/jquery",
		"underscore": "lib/underscore-amd/underscore",
		"backbone": "lib/backbone-amd/backbone",
		"handlebars": "lib/handlebars/handlebars",
		"icanhazjs": "lib/icanhazjs/iCanHaz",
		"openlayers": "lib/openlayers/OpenLayers",
		"d3": "lib/d3/d3",
		"jquery.bootstrap": "lib/bootstrap/dist/js/bootstrap",
		"jquery.slider": "lib/jquery-simple-slider/js/simple-slider",
        "jquery.switch": "lib/bootstrap-switch/static/js/bootstrap-switch",
        "text" : "lib/requirejs-text/text",
        "d3-dragrect": "lib/d3-dragrect/lib/d3-dragrect"
    }
})