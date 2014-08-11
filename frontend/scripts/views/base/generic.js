var Backbone = require('backbone');
var Handlebars = require('handlebars');

GenericView = Backbone.View.extend({
	initialize: function(options){
		this.options = options
		console.log(options)
		this.parent = this.options.parent;
    	this.map = this.parent.map;
	},
	assign : function (view, selector) {
		//http://ianstormtaylor.com/rendering-views-in-backbonejs-isnt-always-simple/
		    view.setElement(this.$(selector)).render();
		},
		remove: function() {
			// Empty the element and remove it from the DOM while preserving events
			$(this.el).empty().detach();
			return this;
		},
		compile: function(template){
			this.template = template;
			return this.template;
		},
		destroy_view: function() {
		    //COMPLETELY UNBIND THE VIEW
		    this.undelegateEvents();
		    this.$el.removeData().unbind();
		    //Remove view from DOM
		    this.remove();
		    Backbone.View.prototype.remove.call(this);
		}
});
module.exports = GenericView;
