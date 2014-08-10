define([
	"jquery",
	"backbone",
	'views/page/classify',
	'views/page/map',
	'views/page/chart',
	'views/page/home',
	'views/page/ternary',
	'data'
	], function($, Backbone, ClassifyPage, MapPage, ChartPage, IndexPage, TernaryPage, DataManager){

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
	        "chart": "chart",
	        "ternary(/:system)": "ternary"
	    },
	    index: function(){
	    	new IndexPage({el: "body"})
	    },
	    classify: function(sample){
	    	new ClassifyPage({el: "body", sample: sample});
	    },
	    map: function(sample, point, tag){
			new MapPage({el: "body", sample: sample, point: point, tag: tag});
	    },
	    chart: function(){
			new ChartPage({el: "body"});
	    },
	    ternary: function(system){
	    	system = system || "pyroxene";
			new TernaryPage({el: "body", system: system});
	    }
	});
	return Router;
});