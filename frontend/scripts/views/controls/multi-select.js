define([
    "jquery",
    "views/base/generic",
    "d3", 
    "options"
    ],function($, GenericView, d3, Options){

    MultiSelectControl = GenericView.extend({
        initialize: function(){
            var a = this;
            this.parent = this.options.parent;
            this.map = this.parent.map;
            this.oxides = Options.oxides;

            var width = $("#tabs").innerWidth();
            //var height = $("#data").innerHeight()-$("#selection_type").height()-$("#tag_manager").height();
            //this.$el.height(height);
            //this.$el.css("overflow","scroll")
            this.$el.css("padding-top", 20);

            this.svg = d3.select(this.el).append("svg")
                .attr("width", width)
            this.width = width;
            this.color = d3.scale.category20()

        },
        render: function(data) {
            a = this;
            nbars = this.map.sel.length;
            var createBar = function(d,i){
                var y = i;
                group = d3.select(this);
                data = a.processData(d);
                var bars = group.selectAll("rect")
                    .data(data)
                    .enter()
                        .append("rect")
                        .attr("x", function(d){return d.off+"%"})
                        .attr("width",function(d){return d.w+"%"})
                        .attr("height",8)
                        .attr("y", 8*i)
                        .attr("fill", function(d,i){ return a.color(i)})

            }

            this.bars = this.svg.selectAll("g.point")
                .data(data, function(d){ return d.properties.id })
            
            this.bars.enter()
                    .append("g")
                    .attr("class","point")
                    .each(createBar);
            this.bars.exit().remove();
            this.svg.attr("height", 8*nbars);
        },
        processData: function(data){
            oxides = data.properties.oxides;
            ob = [];
            for (var key in this.oxides) { v = this.oxides[key]; ob.push(oxides[v]);}
            if (oxides.Total < 100) {
                ob.push(100-oxides.Total);
                var scalar = 1;
            } else {
                var scalar = 100/oxides.Total;
                ob.push(0);
            } 
            var e = 0
            var bb = [];
            for(var i in ob) {
                val = ob[i]*scalar;
                bb.push({"off":e,"w":val})
                e = e+val;
            }
            return bb
        },
        update: function(data){
            this.render(this.map.sel);
        }
    });
    return MultiSelectControl;
});
