define([
    "jquery",
    "views/base/generic", 
    "text!templates/base/sidebar.html",
    "views/controls/registry"
    ],function($,GenericView, template, Controls){

    Sidebar = GenericView.extend({
        initialize: function(){
            this.parent = this.options.parent;
            this.map = this.options.map;
            this.activeTab = "#"+this.options.controls[0]
            this.compile(template);
            this.render();
        },
        render: function(){
            var controls = [];
            console.log(this.options.controls)
            for (var c in this.options.controls){
                console.log(c,this.options.controls[c])
                id = this.options.controls[c];
                control = Controls[id];
                control.id = id;
                controls.push(control);
            }
            opts = {controls: controls};
            this.$el.html(this.template(opts));

            console.log(controls);
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
    return Sidebar;
});
