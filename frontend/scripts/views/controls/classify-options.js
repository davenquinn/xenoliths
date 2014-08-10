var $ = require('jquery');
var GenericView = require('../base/generic');
var Handlebars = require('handlebars');
var Options = require('../../options');
var template = require('../../text!templates/map/classify-options.html');
require('jquery.slider');


OptionsView = GenericView.extend({
	defaults: {
		opacity: 0.7,
		mineral: "ol"
	},
    initialize: function(){
    	this.parent = this.options.parent;
    	this.map = this.parent.map;
    	this.minerals = Options["minerals"];
    	this.template = Handlebars.compile(template);
    	this.render();
    	//this.opacity.bind("slider:changed", this.opacityChanged)
    },
    events: {
    	"change select[name=mineral]": 'mineralChanged',
    	"change input[name=opacity]": 'opacityChanged',
        "change select[name=mode]": 'modeChanged',
        "click button#save": 'save'
    },
    render: function(){
        this.$el.html(this.template({minerals: this.minerals}));
       	this.opacity = $("input[name=opacity]")
       		.simpleSlider({range: [0,1]})
       		.simpleSlider("setValue", this.defaults.opacity);
        return this;
    },
    mineralChanged: function(event){
    	min = $(event.currentTarget).val();
    	this.map.onChangeMineral(min);
    	//this.parent.trigger("change:mineral",min);
    	return false;
    },
    modeChanged: function(event){
        mode = $(event.currentTarget).val();
        if (mode == "draw") this.map.setDraw(true);
        else this.map.setDraw(false);
        return false;
    },
    opacityChanged: function(event){
    	this.map.onChangeOpacity(event.value);
    	//this.parent.trigger("change:opacity",event.value);
    	return false;
    },
    save: function(event){
        this.parent.onSaved();
    }
});
module.exports = OptionsView;

