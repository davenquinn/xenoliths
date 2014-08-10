var $ = require('jquery');
var Class = require('../../lib/classy/classy');
var d3 = require('d3');
var Options = require('../../options');


ColorMap = Class.$extend({

});

ColorMaps = {
    "oxide_total": ColorMap.$extend({
        __init__: function(options){
            var a = this
            this.values = d3.scale.sqrt().domain([0,10]).range(["#71eeb8","salmon"]);
            this.func = function(d){
                return a.values(100-d.properties.oxides.Total);
            };               
        }
    }),
    "oxide": ColorMap.$extend({
        __init__: function(options){
            var a = this;
            this.oxide = options.oxide;
            this.data = options.data;
            this.domain = d3.extent(this.data.features, function(d) {
                return d.properties.oxides[a.oxide] 
            });
            this.values = d3.scale.linear().domain(this.domain).range(["#71eeb8","salmon"]);
            this.func = function(d){
                return a.values(d.properties.oxides[a.oxide])
            }
        }
    }),
    "samples": ColorMap.$extend({
        __init__: function(options){
            var a = this;
            this.values = Options.samples
            this.func = function(d){
                return a.values[d.properties.sample].color;
            }               
        }
    }),
    "minerals": ColorMap.$extend({
        __init__: function(options){
            var a = this;
            this.values = Options.minerals
            this.func = function(d){
                return a.values[d.properties.mineral].color;
            }               
        }
    })
};
module.exports = ColorMaps;

