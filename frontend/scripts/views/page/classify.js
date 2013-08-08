define([
    "views/base/generic",
    "views/map/classify",
    "views/map/classify-options",
    "views/map/select",
    "text!templates/page/classify.html",
    ],function(GenericView, MapPanel, Options, SelectMap, template){

    ClassifyPage = GenericView.extend({
        initialize: function(){
            this.sample = "CK-2";
            this.manager = this.options.manager;
            this.compile(template)
            this.setup()
        },
        setup: function(){
            var self = this;
            this.manager.JSON_RPC("get_classification",{sample: self.sample},function(data,err){
                self.data = data.result;
                console.log(data);
                self.render();
            });
        },
        render: function(){
            this.$el.html(this.template);

            this.map = new MapPanel({el: "#map", parent: this, sample: this.sample, data: this.data});
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
            window.dataManager.JSON_RPC("save_classification",{
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
