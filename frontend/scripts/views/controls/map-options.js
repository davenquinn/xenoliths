define([
	"views/base/generic",
	"views/controls/registry",
    "views/controls/select-map",
    "views/controls/change-colormap"
	], function(GenericView, Controls, SelectMap, ChangeColormap){

    MapOptions = GenericView.extend({
        initialize: function(){
            //this.__super__.initialize.apply(this,arguments)
        	this.parent = this.options.parent;
        	this.map = this.parent.map
        	this.render();
            new SelectMap({
                el: "#select-map",
                parent: this.parent
            });
            new ChangeColormap({
                el: "#colormap",
                parent: this.parent
            });           
        },
        render: function(){
            this.$el.html('<div id="select-map"></div><div id="colormap"></div>');
            return this;
        },
    });
    return MapOptions;
});
