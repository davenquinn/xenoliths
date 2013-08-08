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
        "text" : "lib/requirejs-text/text"
    }
});

require([
    'jquery',
	'backbone',
	'router'
	],function($,Backbone,Router){
        console.log("Starting to get data");
        $("body").append("<img class='loading' src='/static/images/ajax-loader.gif' />");
        $.ajax({
            url: "/data.json",
            dataType:"json",
            success: function(data){
                console.log("Got data");
                window.data = data;
                $("body").html("");
                router = new Router();
                Backbone.history.start();
            },
            error: function(request, textStatus, errorThrown) {
                console.log(textStatus);
                console.log(errorThrown);
            }
        });

});
