var $ = require('jquery');
var GenericView = require('./generic');
var template = require('../../templates/base/sidebar.html');
var Controls = require('../controls/registry');


Sidebar = GenericView.extend({
    initialize: function(options){
        this.options = options;
        this.parent = this.options.parent;
        this.map = this.parent.map;
        this.activeTab = "#"+this.options.controls[0]
        this.compile(template);
        this.render();
    },
    render: function(){
        var controls = [];
        for (var c in this.options.controls){
            id = this.options.controls[c];
            control = Controls[id];
            control.id = id;
            controls.push(control);
        }
        opts = {controls: controls};
        this.$el.html(this.template(opts));

        for (var c in controls){
            control = controls[c];
            control = new control.obj({
                el: "#"+control.id,
                parent: this,
                map: this.map
            });
        }
        this.viewTab(this.activeTab);
    },
    refresh: function(){
        for (var c in this.controls){
            this.controls[c].remove();
        }
        this.render();
    },
    events: {
        "click .navbar-nav a": "onNav"
    },
    onNav: function(event){
        val = event.currentTarget.hash;
        this.activeTab = val;
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
module.exports = Sidebar;
