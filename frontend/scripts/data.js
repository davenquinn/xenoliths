define([
	"jquery",
	"classy",
	'options',
	], function($, Class, Options){

    var Data = Class.$extend({
        __init__: function(data){
            this.data = data;
        },
        filter: function(options){
            var data = this.data;
            var newFeatures = this.data.features;
            $.each(["samples","minerals"], function(i,item){
	            if (typeof(options[item]) !== 'undefined'){
	                if (typeof(options[item]) !== "array") {
	                    if (typeof(options[item]) === "string") {
	                    	options[item] = [options[item]];
	                	}
	                }
	            }            	
            });
            if (typeof(options["bad"]) === 'undefined') options["bad"] = true;

            var newFeatures = []
            $.each(this.data.features, function(i,d){
            	var c1 = true;
            	var c2 = true;
            	var c3 = true;
                if (typeof(options["samples"]) !== 'undefined') {
                	c1 = $.inArray(d.properties.sample, options["samples"]) > -1
               	}
               	if (typeof(options["minerals"]) !== 'undefined') {
                	c2 = $.inArray(d.properties.mineral, options["minerals"]) > -1 
            	}
            	if (options["bad"] == false) {
                    c3 = d.properties.tags.indexOf("bad") == -1;
                }
                if (c1 && c2 && c3) newFeatures.push(d);
            });
            return {
                type: "FeatureCollection",
                features: newFeatures
            };
        }
    });
	return Data;
});