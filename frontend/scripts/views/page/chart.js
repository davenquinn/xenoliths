var BasePage = require('./base');
var ChartPanel = require('../chart/chart');
var Sidebar = require('../base/sidebar');
var template = require('../../templates/page/chart.html');


ChartPage = BasePage.extend({
    initialize: function(options){
        this.options = options;
        this.axes = {x:"oxides.MgO",y:"oxides.FeO"};
        this.filter = {};
        this.parent = options.parent
        this.compile(template)
        this.setup()
    },
    setup: function(){
        this.data = App.Data.filter(this.filter);
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
module.exports = ChartPage;
