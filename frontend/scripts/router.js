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
			this.manager = new DataManager();
			window.dataManager = this.manager;
		},	
	    routes: {
	        '': 'index',
	        'classify(/:sample)': 'classify',
	        'map(/:sample)(/point/:point)': 'map',
	        'map(/:sample)/tag(/:tag)': 'map',
	        "chart": "chart"
	    },
	    index: function(){
	        $(document.body).append("Index route has been called..");
	    },
	    classify: function(sample){
	    	new ClassifyPage({el: "body", sample: sample});
	    },
	    map: function(sample, point, tag){
			new MapPage({el: "body", sample: sample, point: point, tag: tag});
	    },
	    chart: function(){
			new ChartPage({el: "body", manager: this.manager});
	    },
	});
	return Router;
});