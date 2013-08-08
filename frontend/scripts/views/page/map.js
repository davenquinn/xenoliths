define([
    "views/page/base",
    "views/map/map",
    "views/map/map-options",
    "views/map/select",
    "views/controls/data-frame",
    "views/controls/raw-data",
    "text!templates/page/map.html",
    ],function(GenericView, MapPanel, Options, SelectMap, DataFrame, RawViewer,template){

    MapPage = GenericView.extend({
        initialize: function(){
            this.sample = "CK-2";
            this.manager = this.options.manager;
            this.compile(template)
            this.activeTab = "#data"
            this.setup()
        },
        events: {
            "click .navbar-nav a": "onNav"
        },
        setup: function(){
            var self = this;
            this.data = this.manager.filterData({sample: this.sample});
            this.render();
            this.map.dispatcher.on("updated",function(d){
                self.raw.update(d)
                if (self.activeTab=="#data") self.dframe.update(d)
            });
            self.raw.update(data.features[0])
            if (self.activeTab=="#data") this.dframe.update(data.features[0])
        },
        render: function(){
            this.$el.height($(window).height());
            this.$el.html(this.template);
            this.map = new MapPanel({el: "#map", parent: this, sample: this.sample, data: this.data});
            this.sel = new SelectMap({el: "#select_map", parent: this});
            this.raw = new RawViewer({el: "#raw", parent:this})
            this.opt = new Options({el: "#filter", parent: this});
            this.dframe = new DataFrame({el:"#data",parent:this})
            this.sel.setSelected(this.sample);
            this.viewTab(this.activeTab);
        },
        onNav: function(event){
            val = event.currentTarget.hash;
            console.log(val);

            this.activeTab = val
            this.viewTab(val);
            return false;
        },
        viewTab: function(tab){
            this.$(".navbar-nav li").removeClass("active");
            this.$("#tabs>div").hide()
            this.$("a[href="+tab+"]").parent().addClass("active");
            $(tab).show()
        },
        onSampleChanged: function(sample){
            this.sample = sample;
            this.raw.remove();
            this.map.remove();
            this.sel.remove();
            this.opt.remove();
            this.dframe.remove();
            this.setup()
        },
    });
    return MapPage;
});
