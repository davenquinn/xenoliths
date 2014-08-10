var $ = require('jquery');
var Class = require('./lib/classy/classy');
var Options = require('./options');


var Data = Class.$extend({
    __init__: function(data){
        this.data = data;
        this.tags = [];
    },
    getTags: function(){
        a = this;
        if (this.tags.length > 0) return this.tags;
        $.each(a.data.features, function(i,d){
            $.each(d.properties.tags, function(i,t){
                a.pushTag(t);
            });
        });
        return this.tags;
    },
    pushTag: function(tag){
        if (this.tags.indexOf(tag) == -1) this.tags.push(tag);
    },
    filter: function(options){
        var data = this.data;
        $.each(["samples","minerals"], function(i,item){
            if (typeof(options[item]) == "string")
                options[item] = [options[item]];         	
        });
        arr = this.data.features;
        if (options.samples){
            arr = arr.filter(function(d){
                return options.samples.indexOf(d.properties.sample) > -1;
            });
        } 
        if (options.minerals) {
            arr = arr.filter(function(d){
                return options.minerals.indexOf(d.properties.mineral) > -1;
            });
        }
        if (options.tags) {
            excluded = function(t){return options.tags.exclude.indexOf(t) > -1}
            included = function(t){return options.tags.include.indexOf(t) > -1}
            arr = arr.filter(function(d){
                if (d.properties.tags.some(excluded)) return false;
                else if (d.properties.tags.some(included)) return true;
                else return false;
            });
        }
        return {
            type: "FeatureCollection",
            features: arr
        };
    }
});
	module.exports = Data;
