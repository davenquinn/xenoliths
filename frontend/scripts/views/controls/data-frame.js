define([
    "jquery",
    "views/base/generic", 
    "views/controls/oxides",
    "views/controls/raw-data",
    "text!templates/controls/data-frame.html",
    ],function($, GenericView, OxidesWheel, RawData,template){

    DataFrame = GenericView.extend({
        initialize: function(){
            var a = this;
            this.compile(template)
            this.render()
            this.oxides = new OxidesWheel({el: "#oxides",parent: this})
        },
        render: function(){
            this.$el.html(this.template);
            return this
        },
        update: function(data){
            this.data = data;
            this.$("h2.name").html(data.properties.sample+" "+data.properties.id);
            this.oxides.update(data)
        },
    });
    return DataFrame;
});
