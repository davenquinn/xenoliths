define([
	"jquery",
	"views/base/generic",
	"handlebars",
	"options",
	"text!templates/map/select-map.html",
	], function($, GenericView, Handlebars, Options, template){

    SelectMapView = GenericView.extend({
    	defaults: {
    		sample: "CK-2"
    	},
        initialize: function(){
        	this.parent = this.options.parent;
        	this.map = this.parent.map;
        	this.samples = Options["samples"];
        	this.template = Handlebars.compile(template);
        	this.render();
        },
        events: {
        	"change select[name=sample]": 'sampleChanged',
        },
        render: function(){
            this.$el.html(this.template({samples: this.samples}));
            return this;
        },
        sampleChanged: function(event){
        	smp = $(event.currentTarget).val();
        	this.parent.onSampleChanged(smp);
        },
        setSelected: function(sample){
            this.$("select[name=sample]").val(sample);
        }
    });
    return SelectMapView;
});
