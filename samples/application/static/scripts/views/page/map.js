define([
    "views/page/base",
    "views/map/map",
    "views/base/sidebar",
    "text!templates/page/map.html",
    ],function(GenericView, MapPanel, Sidebar,template){

    MapPage = GenericView.extend({
        initialize: function(){
            this.sample = this.options.sample
            if (this.sample == null) this.sample = "CK-2";
            this.compile(template)
            this.setup()
        },
        setup: function(){
            this.filter = {samples: [this.sample]};
            this.data = App.Data.filter(this.filter);
            this.render();
        },
        createSelection: function(){
            a = this;
            function isSelected(element, index, array) {
                s = (element.properties.id == a.options.point);
                return s;
            }
            function isTagged(element, index, array) {
                ind = element.properties.tags.indexOf(a.options.tag)
                console.log(ind)
                return (ind > -1)
            }
            var selection = null;
            if (this.options.tag) selection = this.data.features.filter(isTagged)
            if (this.options.point) selection = this.data.features.filter(isSelected)
            console.log(selection);

            return selection          
        },
        render: function(){
            this.$el.height($(window).height());
            this.$el.html(this.template);
            this.map = new MapPanel({
                el: "#map",
                parent: this,
                sample: this.sample,
                data: this.data,
                selected: this.createSelection()
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
