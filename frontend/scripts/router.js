define([
	"jquery",
	"backbone",
	'views/page/classify',
	'views/page/map',
	'views/page/chart',
	'data'
	], function($, Backbone, ClassifyPage, MapPage, ChartPage, DataManager){

	Router = Backbone.Router.extend({
		initialize: function(options){
			console.log("Starting router.");
			this.manager = new DataManager();
			window.dataManager = this.manager;
		},	
	    routes: {
	        '': 'index',
	        'classify': 'classify',
	        'map': 'map',
	        "chart": "chart"
	    },
	    index: function(){
	        $(document.body).append("Index route has been called..");
	    },
	    classify: function(){
	    	new ClassifyPage({el: "body", manager: this.manager});
	    },
	    map: function(){
			new MapPage({el: "body", manager: this.manager});
	    },
	    chart: function(){
			new ChartPage({el: "body", manager: this.manager});
	    },
	});
	return Router;
});