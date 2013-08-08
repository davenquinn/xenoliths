define([
	"jquery",
	"views/base/generic",
	"options",
	"text!templates/controls/filter.html",
	], function($, GenericView, Options, template){

    FilterData = GenericView.extend({
        initialize: function(){
        	this.parent = this.options.parent;
        	this.map = this.parent.map;
            /*if (this.sample === typeof("undefined")) {
                this.show_samples = true;
            } else this.show_samples = false;*/
        	this.samples = Options["samples"];
        	this.compile(template);
        	this.render();
        },
        events: {
        	"click  button.filter": 'filterData'
        },
        render: function(){
            this.$el.html(this.template({samples: this.samples}));
            return this;
        },
        filterData: function(event){
            console.log(event)
        }
    });
    return FilterData;
});
