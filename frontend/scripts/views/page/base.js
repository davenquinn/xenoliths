define([
    "jquery",
    "views/base/generic"
    ],function($, GenericView){

    GenericPage = GenericView.extend({
        events: {
            "click .navbar-nav a": "onNav"
        },
        onNav: function(event){
            val = event.currentTarget.hash;
            this.activeTab = val
            this.viewTab(val);
            return false;
        },
        viewTab: function(tab){
            this.$(".navbar-nav li").removeClass("active");
            this.$("#tabs>div").hide()
            this.$("a[href="+tab+"]").parent().addClass("active");
            $(tab).show()
        }
    });
    return GenericPage;
});
