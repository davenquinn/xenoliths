define([
    "views/page/base",
    "views/chart/ternary",
    "views/base/sidebar",
    "text!templates/page/chart.html",
    ],function(BasePage, TernaryPanel, Sidebar, template){

    ChartPage = BasePage.extend({
        initialize: function(){
            this.filter = {};
            this.parent = options.parent;
            this.compile(template);
            this.setup();
        },
        setup: function(){
            this.data = App.Data.filter(this.filter);
            this.render();
        },
        render: function(){
            this.$el.height($(window).height());
            this.$el.html(this.template);
            this.map = new TernaryPanel({
                el: "#chart",
                parent: this,
                data: this.data,
                system: this.options.system
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
