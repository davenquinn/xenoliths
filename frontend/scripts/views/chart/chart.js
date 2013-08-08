define([
    "backbone",
    "d3", 
    "views/base/generic", 
    "options",
    "views/base/colors"
    ],function(Backbone, d3, GenericView, Options, Colorizer){

    Chart = GenericView.extend({
        initialize: function(){
            this.parent = this.options.parent;
            this.axes = this.options.axes;
            this.data = this.options.data;
            this.colormap = new Colorizer["samples"]();
            this.dispatcher = d3.dispatch("updated");


            this.margin = {
                left: 50,
                top: 20,
                bottom: 40,
                right: 0
            }
            this.width = this.$el.width()-this.margin.left-this.margin.right;
            this.height = this.$el.height()-this.margin.top-this.margin.bottom;
            a = this;
            this.onMouseMove = function(d,i) {
                d3.select(".dot.selected")
                    .attr("class","dot")
                d3.select(this)
                    .attr("class","dot selected")
                a.dispatcher.updated(d);
            };
            this.setupEventHandlers();

            this.loadAxes();
        },
        loadAxes: function(){
            var a = this;
            this.x = d3.scale.linear()
                    .domain([-.05, 1.05*d3.max(this.data.features,function(d) {
                        return eval("d.properties."+a.axes.x);
                    })])
                    .range([0, this.width]);
            this.y = d3.scale.linear()
                    .domain([-.05,1.05*d3.max(this.data.features,function(d) {
                        return eval("d.properties."+a.axes.y);})])
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
                .attr("height", this.height);

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

             this.points.selectAll(".dot")
                .data(this.data.features)
                .enter().append("circle")
                    .attr("class", "dot")
                    .attr("r", 3.5)
                    .attr("cx", this.xTransform)
                    .attr("cy", this.yTransform)
                    .on("mouseover", this.onMouseMove)
                    .style("fill", a.colormap.func);

            this.dims = [this.width, this.height]

            this.setupEventHandlers()
        },
        setupEventHandlers: function(){
            var a = this;
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
        },
        setColormap: function(name, options){
            console.log("Setting colormap")
            this.colormap = new Colorizer[name](options);
            this.points.selectAll(".dot").style("fill", a.colormap.func)
        },
        setAxes: function(axes){
            d3.select(this.el).select("svg").remove();
            this.axes = axes;
            this.loadAxes();
        }
    });
    return Chart;
});
