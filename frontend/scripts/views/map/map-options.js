define([
	"jquery",
	"views/base/generic",
	"handlebars",
	"options",
	"text!templates/map/map-options.html",
	"jquery.slider"
	], function($, GenericView, Handlebars, Options, template){

    OptionsView = GenericView.extend({
        initialize: function(){
        	this.parent = this.options.parent;
        	this.map = this.parent.map;
        	this.template = Handlebars.compile(template);
        	this.render();
        	//this.opacity.bind("slider:changed", this.opacityChanged)
        },
        events: {
            "change select[name=colormap]": 'changeColormap',
        },
        render: function(){
            this.$el.html(this.template({oxides: Options.oxides}));
            return this;
        },
        changeColormap: function(event){
            val = $(event.currentTarget).val();
            if (Options.oxides.indexOf(val) > -1) {
                console.log(val);
                this.map.setColormap("oxide",{oxide:val, data: this.map.data});
            }
            else this.map.setColormap(val)
        }
    });
    return OptionsView;
});
