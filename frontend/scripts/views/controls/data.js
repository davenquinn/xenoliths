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
            this.$("#multiple").hide();
            this.selectMode = "single"
            this.map.dispatcher.on("updated.data",function(d){
                a.update(d);
            });
            if (this.map.sel) {
                this.update(this.map.sel[0])
            } else this.update(this.map.data.features[0])
        },
        events: {
            "change #selection_type input": "changeSelectionType"
        },
        changeSelectionType: function(event){
            s = this.selectMode;
            console.log(s)
            this.$("#"+s).hide(300);
            this.selectMode = s == "single" ? "multiple" : "single";
            this.$("#"+this.selectMode).show(300);
            this.map.setSelectMode(this.selectMode);
        },
        render: function(){
            this.$el.html(this.template);
            this.$("#selection").bootstrapSwitch();
            return this
        },
        update: function(data){
            this.tags.update(this.map.sel);
            if (this.map.selectMode == "multiple") {
                this.data = this.map.sel
                this.multiSelect.update(data);
            } else {
                this.data = data;
                if (data == null) return;
                id = data.properties.id;
                sample = data.properties.sample;
                this.$(".id").html(id);
                this.$(".sample").html(sample);
                this.$(".map-link").attr("href","#map/"+sample+"/point/"+id)          
                this.oxides.update(data)
            }
            //this.formula.update(data)
        },
    });
    return DataFrame;
});
