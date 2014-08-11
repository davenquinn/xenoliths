var $ = require('jquery');
var GenericView = require('../base/generic');
var OxidesWheel = require('./oxides');
var MultiSelect = require('./multi-select');
var TagManager = require('./tag-manager');
var template = require('../../templates/controls/data-frame.html');
var Options = require('../../options');
require('bootstrap-switch');


DataFrame = GenericView.extend({
    initialize: function(options){
        this.options = options;
        var a = this;
        this.map = this.options.map;
        this.compile(template)
        this.render()
        this.oxides = new OxidesWheel({el: "#oxides",parent: this})
        this.tags = new TagManager({el: "#tag_manager", parent:this})
        this.multiSelect = new MultiSelect({el: "#multiple",parent: this})
        this.tdata = null;

        if (this.map.sel) {
            this.update(this.map.sel[0])
        } else this.update(this.map.data.features[0])

        this.map.dispatcher.on("updated.data",function(d){
            sel = d3.select(this);
            if (sel.classed("selected")) a.tdata = d;
            a.update(d);
        });
        this.map.dispatcher.on("mouseout", function(d){
            sel = d3.select(this)
            a.update(null);
        });
    },
    render: function(){
        this.$el.html(this.template);
        return this
    },
    update: function(data){
        if (data == null) {
            this.tags.update(this.map.sel);
            data = this.tdata;
        } else {
            this.tags.update([data])
        }
        this.multiSelect.update(this.map.sel);

        if (data == null) return;
        id = data.properties.id;
        sample = data.properties.sample;
        this.$(".id").html(id);
        this.$(".sample").html(sample);
        this.$(".map-link").attr("href","#map/"+sample+"/point/"+id)
        this.oxides.update(data)
    },
});
module.exports = DataFrame;
