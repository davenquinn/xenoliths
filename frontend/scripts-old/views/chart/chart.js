define([
    "backbone",
    "d3", 
    "views/base/generic", 
    "options",
    "views/base/colors",
    ],function(Backbone, d3, GenericView, Options, Colorizer){

    Chart = GenericView.extend({
        initialize: function(){
            this.parent = this.options.parent;
            this.axes = this.options.axes;
            this.data = this.options.data;
            this.colormap = new Colorizer["samples"]();
            this.sel = this.options.selected;
            if (!this.sel) this.sel = [];

            this.margin = {
                left: 50,
                top: 20,
                bottom: 40,
                right: 0
            }
            this.width = this.$el.width()-this.margin.left-this.margin.right;
            this.height = this.$el.height()-this.margin.top-this.margin.bottom;

            this.setupEventHandlers();
            this.loadAxes();
        },
        loadAxes: function(){
            var a = this;
            minfunc = function(axes) {
                axfunc = function(d) { return eval("d.properties."+axes)}
                max = d3.max(a.data.features,axfunc);
                min = d3.min(a.data.features,axfunc);
                rng = max-min;
                return min - 0.02*rng;
            };
            maxfunc = function(axes) {
                axfunc = function(d) { return eval("d.properties."+axes)}
                max = d3.max(a.data.features,axfunc);
                min = d3.min(a.data.features,axfunc);
                rng = max-min;
                return max + 0.02*rng;
            };
            this.x = d3.scale.linear()
                    .domain([minfunc(this.axes.x), maxfunc(this.axes.x)])
                    .range([0, this.width]);
            this.y = d3.scale.linear()
                    .domain([minfunc(this.axes.y), maxfunc(this.axes.y)])
                    .range([this.height, 0]);

            this.xAxis = d3.svg.axis()
                .scale(this.x)
                .orient("bottom")
                .tickSize(-this.height);

            this.yAxis = d3.svg.axis()
                .scale(this.y)
                .orient("left")
                .ticks(5)
                .tickSize(-this.width)

            this.zoomer = d3.behavior.zoom()
                .x(this.x).y(this.y)
                .scaleExtent([1, 40])
                .on("zoom", this.onZoom);

            this.drawSVG()
        },
        drawSVG: function(){
            var a = this;
            this.svg = d3.select(this.el).append("svg")
                    .attr("width", this.$el.width())
                    .attr("height", this.$el.width())
                    .append("g")
                        .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")
                        .call(this.zoomer);

            this.svg.append("rect")
                .attr("id", "clip")
                .attr("width", this.width)
                .attr("height", this.height)
                .on("click", this.onBackgroundClick);

            this.svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + this.height + ")")
                .call(this.xAxis)
                .append("text")
                    .attr("class", "label")
                    .attr("x", this.width/2)
                    .attr("y", 30)
                    .style("text-anchor", "center")
                    .text(this.axes.x);

            this.svg.append("g")
                .attr("class", "y axis")
                .call(this.yAxis)
                .append("text")
                  .attr("class", "label")
                  .attr("transform", "rotate(-90)")
                  .attr("y", -40)
                  .attr("x", -this.height/2)
                  .attr("dy", ".71em")
                  .style("text-anchor", "center")
                  .text(this.axes.y)


            var clip = this.svg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("id", "clip-rect")
                .attr("x", "0")
                .attr("y", "0")
                .attr("width", this.width)
                .attr("height", this.height)

             this.points = this.svg.append("g")
                .attr("class","data")
                .attr("clip-path", "url(#clip)");

             this.points.call(this.joinData, this.data);


            this.dims = [this.width, this.height]

        },
        setupEventHandlers: function(){
            var a = this;

            this.dispatcher = d3.dispatch("updated", "mouseout");
            this.onMouseMove = function(d,i) {
                d3.selectAll(".dot.hovered").classed("hovered", false)

                sel = d3.select(this);
                if (d3.event.shiftKey && !sel.classed("selected")){
                    sel.classed("selected",true)
                    a.sel.push(d)
                }
                sel.classed("hovered", true);
                a.dispatcher.updated.apply(this,arguments);
            };
            this.onMouseOut = function(d,i){
                sel = d3.select(this);
                if (a.sel.length > 0) {
                    sel.classed("hovered", false)
                    a.dispatcher.mouseout.apply(this,arguments);
                };
            };
            this.onClick = function(d,i) {
                item = d3.select(this)
                toSelect = !item.classed("selected")
                item.classed("selected", toSelect)
                if (toSelect) {
                    a.sel.push(d)
                } else {
                    var index = a.sel.indexOf(d);
                    a.sel.splice(index,1);
                }
                a.dispatcher.updated.apply(this,arguments);

                d3.event.stopPropagation();
            };
            this.onBackgroundClick = function(d,i){
                d3.selectAll(".dot.selected").classed("selected",false);
                d3.event.stopPropagation();
                a.sel.length = 0;
                a.dispatcher.updated.apply(this,arguments);
            };

            this.xTransform = function(d) { return a.x(eval("d.properties."+a.axes.x)); }
            this.yTransform = function(d) { return a.y(eval("d.properties."+a.axes.y)); }
            this.onZoom = function(){
                var translate = a.zoomer.translate(),
                    scale = a.zoomer.scale();

                tx = Math.min(0, Math.max(a.dims[0] * (1 - scale), translate[0]));
                ty = Math.min(0, Math.max(a.dims[1] * (1 - scale), translate[1]));

                a.zoomer.translate([tx, ty]);
                a.svg.select(".x.axis").call(a.xAxis);
                a.svg.select(".y.axis").call(a.yAxis);
                a.svg.selectAll(".dot")
                    .attr("cx", a.xTransform)
                    .attr("cy", a.yTransform)
            }
            this.joinData = function(element, data){
                var dot = element.selectAll(".dot")
                    .data(data.features);
                dot.exit().remove();
                dot.enter().append("circle")
                    .attr("class", "dot")
                    .attr("r", 3.5)
                    .attr("cx", a.xTransform)
                    .attr("cy", a.yTransform)
                    .on("mouseover", a.onMouseMove)
                    .on("click", a.onClick)
                    .on("mouseout", a.onMouseOut)
                    .style("fill", a.colormap.func);   
            };
        },
        setColormap: function(name, options){
            this.colormap = new Colorizer[name](options);
            this.points.selectAll(".dot").style("fill", this.colormap.func)
        },
        refresh: function() {
            d3.select(this.el).select("svg").remove();
            this.loadAxes()
        },
        setAxes: function(axes){
            this.axes = axes;
            this.refresh()
        },
        setData: function(data){
            this.data = data;
            this.refresh()
        }
    });
    return Chart;
});
