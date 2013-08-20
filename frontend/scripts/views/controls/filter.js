define([
	"jquery",
	"views/base/generic",
	"options",
    "app",
	"text!templates/controls/filter.html",
	], function($, GenericView, Options, App, template){

    $.fn.serializeObject = function()
    {
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
            a = this;
            this.$el.html(this.template({
                samples: this.samples,
                minerals: Options.minerals
            }));
            $.each(["minerals","samples"],function(i,d){
                condition = a.$("input[name=filter-"+d+"]").is(":checked");
                console.log(condition);
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
            arr["bad"] = arr["bad"] == "on" ? true : false;
            console.log(arr)
            data = window.App.Data.filter(arr);
            this.map.setData(data);
        }
    });
    return FilterData;
});
