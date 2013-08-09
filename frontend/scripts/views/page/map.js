define([
    "views/page/base",
    "views/map/map",
    "views/base/sidebar",
    "text!templates/page/map.html",
    ],function(GenericView, MapPanel, Sidebar,template){

    MapPage = GenericView.extend({
        initialize: function(){
            this.sample = "CK-2";
            this.manager = this.options.manager;
            this.compile(template)
            this.setup()
        },
        setup: function(){
            this.data = this.manager.filterData({sample: this.sample});
            this.render();
        },
        render: function(){
            this.$el.height($(window).height());
            this.$el.html(this.template);
            this.map = new MapPanel({
                el: "#map",
                parent: this,
                sample: this.sample,
                data: this.data
            });
            this.sidebar = new Sidebar({
                el:"#sidebar",
                parent: this,
                controls: ["data", "raw", "map-options", "filter"]
            });
        },
        onSampleChanged: function(sample){
            this.sample = sample;
            this.map.remove();
            this.sidebar.refresh();
            this.setup()
        },
    });
    return MapPage;
});
