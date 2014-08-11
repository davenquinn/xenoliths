var $ = require('jquery');
var Backbone = require('backbone');
var ClassifyPage = require('./views/page/classify');
var MapPage = require('./views/page/map');
var ChartPage = require('./views/page/chart');
var IndexPage = require('./views/page/home');
var TernaryPage = require('./views/page/ternary');
var DataManager = require('./data');


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
	module.exports = Router;
