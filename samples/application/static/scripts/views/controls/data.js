define([
    "jquery",
    "views/base/generic", 
    "views/controls/oxides",
    "views/controls/multi-select",
    "views/controls/tag-manager",
    "text!templates/controls/data-frame.html",
    "options",
    "jquery.switch"
    ],function($, GenericView, OxidesWheel, MultiSelect, TagManager, template, Options){

    DataFrame = GenericView.extend({
        initialize: function(){
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
    return DataFrame;
});
