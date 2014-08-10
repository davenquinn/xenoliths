var $ = require('jquery');
var GenericView = require('../base/generic');
var Options = require('../../options');
var template = require('../../text!templates/chart/chart-options.html');
require('jquery.slider');


OptionsView = GenericView.extend({
    initialize: function(){
        this.parent = this.options.parent;
        this.map = this.parent.map;
        this.compile(template);
        this.render();
    },
    events: {
        "change select[name=colormap]": 'changeColormap',
        "click  button.axes": 'changeAxes'
    },
    render: function(){
        this.$el.html(this.template({oxides: Options.oxides}));
        return this;
    },
    changeColormap: function(event){
        val = $(event.currentTarget).val();
        if (Options.oxides.indexOf(val) > -1) {
            this.map.setColormap("oxide",{oxide:val, data: this.map.data});
        }
        else this.map.setColormap(val)
    },
    changeAxes: function(event){
        axes = {
            x:this.$("#x-axis").val(),
            y:this.$("#y-axis").val()
        }   
        this.map.setAxes(axes)
        return false;
    }
});
module.exports = OptionsView;

