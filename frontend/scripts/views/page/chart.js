define([
    "views/page/base",
    "views/chart/chart",
    "views/base/sidebar",
    "text!templates/page/chart.html",
    ],function(BasePage, ChartPanel, Sidebar, template){

    ChartPage = BasePage.extend({
        initialize: function(){
            this.axes = {x:"oxides.MgO",y:"oxides.FeO"};
            this.filter = {};
            this.manager = this.options.manager;
            this.parent = options.parent
            this.compile(template)
            this.setup()
        },
        setup: function(){
            var self = this;
            this.data = this.manager.filterData(this.filter);
            this.render();
        },
        render: function(){
            this.$el.height($(window).height());
            this.$el.html(this.template);
            this.map = new ChartPanel({
                el: "#chart",
                parent: this,
                data: this.data,
                axes: this.axes
            });
            this.sidebar = new Sidebar({
                el:"#sidebar",
                map: this.map,
                parent: this,
                controls: ["data", "raw", "chart-options", "filter"]
            });
        },
        refresh: function(){
            this.map.remove();
            this.setup()
            this.sidebar.refresh();
        }
    });
    return ChartPage;
});
