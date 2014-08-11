var $ = require('jquery');
var GenericView = require('../base/generic');
var Options = require('../../options');
var template = require('../../templates/controls/change-colormap.html');


ChangeColormap = GenericView.extend({
    initialize: function(options){
        this.options = options;
    	this.parent = this.options.parent;
    	this.map = this.parent.map;
    	this.compile(template);
    	this.render();
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
module.exports = ChangeColormap;
