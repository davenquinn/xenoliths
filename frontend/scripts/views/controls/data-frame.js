define([
    "jquery",
    "views/base/generic", 
    "views/controls/oxides",
    "text!templates/controls/data-frame.html",
    "options"
    ],function($, GenericView, OxidesWheel,template, Options){

    DataFrame = GenericView.extend({
        initialize: function(){
            var a = this;
            this.map = this.options.map;
            console.log("Data frame");
            this.compile(template)
            this.render()
            this.oxides = new OxidesWheel({el: "#oxides",parent: this})
            this.map.dispatcher.on("updated.data",function(d){
                a.update(d);
            });
        },
        render: function(){
            this.$el.html(this.template);
            return this
        },
        update: function(data){
            this.data = data;
            this.$(".id").html(data.properties.id);
            this.$(".sample").html(data.properties.sample);
            mineral = Options.minerals[data.properties.mineral]
            this.$(".mineral").html(mineral.name);            
            this.oxides.update(data)
        },
    });
    return DataFrame;
});
