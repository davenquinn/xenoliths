require.config({
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
    urlArgs: "bust=" +  (new Date()).getTime(),
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
});

require([
    'jquery',
	'backbone',
    'app',
	],function($,Backbone,startApp){
        console.log("Starting to get data");
        $("body").append("<img class='loading' src='/static/images/ajax-loader.gif' />");
        $.ajax({
            url: "/data/data.json?bust=" +  (new Date()).getTime(),
            dataType:"json",
            success: startApp,
            error: function(request, textStatus, errorThrown) {
                console.log(textStatus);
                console.log(errorThrown);
            }
        });

});
