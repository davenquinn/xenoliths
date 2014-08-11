var BasePage = require('./base');
var ChartPanel = require('../chart/chart');
var Sidebar = require('../base/sidebar');
var template = require('../../templates/page/home.html');


IndexPage = BasePage.extend({
    initialize: function(){
        this.compile(template)
        this.render()
    },
    render: function(){
        this.$el.html(this.template);        }
});
module.exports = IndexPage;
