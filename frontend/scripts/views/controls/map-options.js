var GenericView = require('../base/generic');
var Controls = require('./registry');
var SelectMap = require('./select-map');
var ChangeColormap = require('./change-colormap');


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
module.exports = MapOptions;

