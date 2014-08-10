var $ = require('jquery');
var d3 = require('d3');
var GenericView = require('../base/generic');
var Options = require('../../options');


TagFilter = GenericView.extend({
    initialize: function(){
        this.tags = window.App.Data.getTags();
        this.render();
    },
    render: function(){
        this.$el
            .append('<ul id="tag-filterlist"></ul>')
            .append('<div class="controls"><a href="#all">Select All</a><a href="#none">Select None</a><a href="#bad">Exclude Bad</a></div>')
        this.ul = d3.select("#tag-filterlist")
        this.ul.call(this.bindData,this.prepareData())
        return this
    },
    events: {
        "click li": "changeTag",
        "click a": "selectData"
    },
    prepareData: function() {
        this.data = this.tags.map(function(item){
            return {
                "name": item,
                "sel": true
            }
        });
        return this.data;
    },
    selectData: function(event){
        v = event.target.href.split("#")[1]
        if (v == "all") {
            this.data.forEach(function(d){ d.sel = true;})
        } else if (v == "none") {
            this.data.forEach(function(d){ d.sel = null; })
        } else if (v == "bad") {
            this.data.forEach(function(d){
                if (Options.bad_tags.indexOf(d.name) > -1) {
                    d.sel = false;
                }
            })
        }
        this.ul.call(this.bindData,this.data);
        return false;
    },
    bindData: function(ul, data) {
        li = ul.selectAll("li")
            .data(data, function(d){
                return d.name;
            });
        li.enter()
            .append("li")
            .html(function(d) { return d.name; });
        li.attr("class",function(d){
                if (d.sel == null) return "ignore";
                else return d.sel ? "include" : "exclude";
            });
    },
    getFilter: function(){
        var reduce = function(d){return d.name}; 
        return {
            include: this.data.filter(function(d){return d.sel}).map(reduce),
            exclude: this.data.filter(function(d){return d.sel == false}).map(reduce)
        }
    },
    changeTag: function(event){
        d = event.currentTarget.__data__
        //var d = this.data[this.data.indexOf(data)];
        if (d.sel == null) d.sel = false;
        else d.sel = d.sel ? null : true;
        this.ul.call(this.bindData,this.data);
    }
});
module.exports = TagFilter;

