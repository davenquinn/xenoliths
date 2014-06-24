define([
    "views/page/base",
    "views/chart/chart",
    "views/base/sidebar",
    "text!templates/page/home.html",
    ],function(BasePage, ChartPanel, Sidebar, template){

    IndexPage = BasePage.extend({
        initialize: function(){
            this.compile(template)
            this.render()
        },
        render: function(){
            this.$el.html(this.template);        }
    });
    return IndexPage;
});
