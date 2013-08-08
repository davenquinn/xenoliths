define([
    "views/page/base",
    "views/chart/chart",
    "views/chart/chart-options",
    "views/controls/data-frame",
    "views/controls/raw-data",
    "text!templates/page/chart.html",
    ],function(BasePage, ChartPanel, Options, DataFrame, RawViewer,template){

    GraphPage = BasePage.extend({
        initialize: function(){
            this.axes = {x:"oxides.MgO",y:"oxides.FeO"};
            this.filter = {};
            this.manager = this.options.manager;
            this.parent = options.parent
            this.compile(template)
            this.activeTab = "#data"
            this.setup()
        },
        setup: function(){
            var self = this;
            this.data = this.manager.filterData(this.filter);
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
            this.map = new ChartPanel({el: "#chart", parent: this, data: this.data, axes: this.axes});
            this.raw = new RawViewer({el: "#raw", parent: this})
            this.opt = new Options({el: "#controls", parent: this, map: this.map});
            this.dframe = new DataFrame({el:"#data",parent:this})
            this.viewTab(this.activeTab);
        },
        refresh: function(){
            this.raw.remove();
            this.map.remove();
            this.opt.remove();
            this.dframe.remove();
            this.setup()
        }
    });
    return GraphPage;
});
