var $ = require('jquery');
var GenericView = require('../base/generic');
var Options = require('../../options');
var App = require('../../app');
var TagFilter = require('./tag-filter');
var template = require('../../text!templates/controls/filter.html');


$.fn.serializeObject = function() {
   var o = {};
   var a = this.serializeArray();
   $.each(a, function() {
       if (o[this.name]) {
           if (!o[this.name].push) {
               o[this.name] = [o[this.name]];
           }
           o[this.name].push(this.value || '');
       } else {
           o[this.name] = this.value || '';
       }
   });
   return o;
};

FilterData = GenericView.extend({
    initialize: function(){
    	this.parent = this.options.parent;
    	this.map = this.parent.map;
        /*if (this.sample === typeof("undefined")) {
            this.show_samples = true;
        } else this.show_samples = false;*/
    	this.samples = Options["samples"];
    	this.compile(template);
    	this.render();
    },
    events: {
        "change #filter-settings input": "toggleControls",
    	"click  button.filter": 'filterData'
    },
    render: function(){
        var a = this;
        this.$el.html(this.template({
            samples: this.samples,
            minerals: Options.minerals
        }));
        this.tagFilter = new TagFilter({
            el:this.$("#tag-filter"),
            parent: this
        });
        $.each(["minerals","samples", "tags"],function(i,d){
            condition = a.$("input[name=filter-"+d+"]").is(":checked");
            a.$("div."+d).toggle(condition, {duration: 300});
        });
        return this;
    },
    toggleControls: function(event){
        checked = event.target.checked;
        cls = event.target.name.split('-')[1];
        console.log(cls);
        this.$("."+cls).toggle(checked, {duration: 300});
    },
    filterData: function(event){
        arr = this.$("form").serializeObject();
        $.each(["minerals","samples"],function(i,d){
            if (arr["filter-"+d] != "on") {
                delete arr[d];
            }
            delete arr["filter-"+d];
        });
        if (arr["filter-tags"] == "on") {
            arr["tags"] = this.tagFilter.getFilter();
        }
        console.log(arr)
        data = window.App.Data.filter(arr);
        this.map.setData(data);
    }
});
module.exports = FilterData;

