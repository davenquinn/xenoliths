var $ = require('jquery');
var GenericView = require('../base/generic');
var Options = require('../../options');
var template = require('../../text!templates/map/select-map.html');

SelectMap = GenericView.extend({
	defaults: {
		sample: "CK-2"
	},
    initialize: function(){
    	this.parent = this.options.parent;
    	this.map = this.parent.map;
    	this.samples = Options["samples"];
    	this.compile(template);
        this.currentLayer = "sem";
    	this.render();
    },
    events: {
    	"change select[name=sample]": 'sampleChanged',
        "change .layer-switch": 'changeLayer',
    },
    render: function(){
        this.$el.html(this.template({samples: this.samples}));
        this.setSelected(this.map.sample_name)
        return this;
    },
    sampleChanged: function(event){
    	smp = $(event.currentTarget).val();
    	this.map.parent.onSampleChanged(smp);
    },
    setSelected: function(sample){
        this.$("select[name=sample]").val(sample);
    },
    changeLayer: function(event){
        val = $(event.currentTarget).val();
        lyr = this.currentLayer == "sem" ? "scan" : "sem"; 
        this.map.setLayer(lyr);
        this.currentLayer = lyr;
    }
});
module.exports = SelectMap;

