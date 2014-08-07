define([
    "views/base/generic",
    "views/map/classify",
    "views/controls/classify-options",
    "views/controls/select-map",
    "text!templates/page/classify.html",
    ],function(GenericView, MapPanel, Options, SelectMap, template){

    ClassifyPage = GenericView.extend({
        initialize: function(){
            this.sample = this.options.sample;
            if (this.sample === null) this.sample = "CK-2";
            this.compile(template)
            this.setup()
        },
        setup: function(){
            var self = this;
            App.JSON_RPC("get_classification",{sample: self.sample},function(data,err){
                self.data = data.result;
                console.log(data);
                self.render();
            });
        },
        render: function(){
            this.$el.html(this.template);

            this.map = new MapPanel({el: "#map", parent: this, sample: this.sample});
            this.sel = new SelectMap({el: "#select_map", parent: this});
            this.opt = new Options({el: "#options", parent: this});
            this.sel.setSelected(this.sample);
        },
        onSampleChanged: function(sample){
            this.sample = sample;
            this.map.remove();
            this.sel.remove();
            this.opt.remove();
            this.setup()
        },
        onSaved: function(){
            App.JSON_RPC("save_classification",{
                sample: this.sample, 
                classification: this.map.getData()
            },function(data,err){
                    self.data = data.result;
                    console.log(data);
            });
        }
    });
    return ClassifyPage;
});