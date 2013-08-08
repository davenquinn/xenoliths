define([
    "jquery",
    "backbone"
    ],function($,Backbone){
    var DataManager = Backbone.Model.extend({
        initialize: function(){
            console.log('Initializing data manager');
            this.data = window.data;
        },
        JSON_RPC: function(method, params, callback){
            var url = "/json/";
            request = {
                method: method,
                params: params,
                jsonrpc: "2.0",
                id: 1
            };
            $.post(url, JSON.stringify(request), callback, "json");
        },
        filterData: function(options){
            var data = this.data;
            if (typeof(options.sample) === 'undefined'){
                var newFeatures = this.data.features;
            } else {
                if (typeof(options.sample) === "array") {
                    samples = options.sample
                } else if (typeof(options.sample) === "string") {
                    samples = [options.sample];
                }
                var newFeatures = []
                $.each(data.features, function(i,d){
                    if (samples.indexOf(d.properties.sample) > -1) newFeatures.push(d);
                });
            }
            return {
                type: "FeatureCollection",
                features: newFeatures
            };
        }
    }); 
    return DataManager;
});

