define([
    "jquery",
    "d3",
    "views/base/generic", 
    "text!templates/controls/tag-manager.html",
    "options"
    ],function($, d3, GenericView, template, Options){

    TagManager = GenericView.extend({
        initialize: function(){
            this.compile(template)
            this.tags = [];
            this.data = [];
            this.render();
        },
        render: function(){
            this.$el.html(this.template);
            this.ul = d3.select("#tag_field")
            //this.ul.call(this.bindData,[])
            return this
        },
        events: {
            "click .icon-remove": "removeTag",
            "click button": "addTag",
            'keypress input[type=text]': 'addTagOnEnter'

        },
        bindData: function(ul, tags) {
            li = ul.selectAll("li")
                .data(tags,function(d) {
                   return tags.indexOf(d);
                });
            li.exit().remove();
            li.enter()
                .append("li")
                .html(function(d) { return d.name; })
                .attr("class",function(d){ return d.all ? "all" : "some"})
                .append("span")
                    .html("<i class='icon-remove'></i>")
                    .attr("class","remove");
        },
        update: function(data){
            this.tags = this.processData(data);
            this.ul.call(this.bindData,this.tags);
        },
        processData: function(data){
            //takes a list of point items and outputs an object containing
            // tags as indices to boolean values for whether the tag is shared
            // by all items.
            this.data = data;
            var nitems = data.length;
            arrays = data.map(function(item){
                return item.properties.tags;
            });
            arr = [].concat.apply([], arrays);
            ndata = arr.reduce(function (acc, curr) {
                  if (typeof acc[curr] == 'undefined') {
                    acc[curr] = 1;
                  } else {
                    acc[curr] += 1;
                  }
                  return acc;
            }, {});
            this.tags.length = 0;
            for(var i in ndata) {
                obj = {
                    name: i,
                    all: ndata[i] >= data.length ? true : false
                };
                this.tags.push(obj);
            }
            console.log(this.tags);
            return this.tags;
        },
        removeTag: function(event){
            data = event.currentTarget.parentNode.__data__
            var tag = data.name;
            var index = this.tags.indexOf(data);
            var elements = [];
            this.tags.splice(index,1);
            for (var i in this.data){
                d = this.data[i];
                tags = d.properties.tags;
                ind = tags.indexOf(tag)
                if (ind != -1) tags.splice(ind, 1);
                elements.push([d.properties.sample,d.properties.id])

            }
            App.JSON_RPC("remove_tag",{
                tag: tag, 
                points: elements
            });
            this.ul.call(this.bindData,this.processData(this.data));

        },
        addTagOnEnter: function(e) {
            if (e.keyCode != 13) return;
            this.addTag();
            return false;
        },
        addTag: function(event){
            arr = this.$("form").serializeObject();
            if (arr.tag == "") return false;
            var tag = arr.tag.toLowerCase()
            var elements = [];
            for (var i in this.data){
                d = this.data[i];
                tags = d.properties.tags;
                if (tags.indexOf(tag) == -1) tags.push(tag);
                elements.push([d.properties.sample,d.properties.id])
            }
            App.JSON_RPC("add_tag",{
                tag: tag, 
                points: elements
            });
            this.ul.call(this.bindData,this.processData(this.data));
            return false;
        }
    });
    return TagManager;
});
