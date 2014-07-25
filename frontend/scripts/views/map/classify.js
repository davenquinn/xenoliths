define([
    "backbone",
    "d3", 
    "views/map/base", 
    "options"
    ],function(Backbone, d3, MapBase, Options){

    ClassifyMap = MapBase.extend({
        initialize: function(){
            ClassifyMap.__super__.initialize.apply(this, arguments);
            this.parent = this.options.parent;
            this.data = this.parent.data;
            this.classifyLayer();
            var div = d3.selectAll("#" + this.overlay.div.id);
            this.svg = div.selectAll("svg");
            this.mineral = "na";
        },
        classifyLayer: function(){
            var a = this;
            var overlay = new OpenLayers.Layer.Vector("classify");

            // Add the container when the overlay is added to the map.
            overlay.afterAdd = function () {
                var project = function(x) {
                    var point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]));
                    return [point.x, point.y];
                }
                var bounds = a.bounds;
                var div = d3.selectAll("#" + overlay.div.id);
                div.selectAll("svg").remove();
                
                var svg = div.append("svg");

                var g = svg.append("svg:g");

                console.log(a.data);
                if (a.data === false) {
                    //build new array
                    cells = 5000;
                    aspect_ratio = -bounds.right/bounds.bottom;
                    y = Math.sqrt(cells/aspect_ratio)
                    x = y.toFixed(0)*aspect_ratio

                    var ccx = x.toFixed(0), // cell count x
                        ccy = y.toFixed(0), // cell count y
                        states = new Array();
                        d3.range(ccx*ccy).forEach(function(i) {
                            states.push({v:"un"})
                        });
                    a.data = {
                        w: ccx,
                        h: ccy,
                        values: states
                    };
                }
                a.mousedown = 0;
                svg.attr("viewBox","0 0 "+a.data.w+" "+a.data.h)

                minerals = Options.minerals;
                var getColor = function(d) {
                    if (d.v == "un") {
                        return "";
                    } else {
                        return minerals[d.v].color;
                    }
                };
                var fillOpacity = function(d){
                    if (d.v == "un") {
                        return "0.0";
                    } else {
                        return "1.0";
                    }
                };
                svg.selectAll("rect")
                    .data(a.data.values)
                    .enter().append("svg:rect")
                        .attr("stroke", "none")
                        .attr("fill", getColor)
                        .attr("fill-opacity", fillOpacity)
                        .attr("x", function(d,i) { return i%a.data.w })
                        .attr("y", function(d,i) { return Math.floor(i/a.data.w)})
                        .attr("width", 1)
                        .attr("height", 1)
                        .on("mousedown", function(d,i){
                            console.log(a.mousedown)
                            if (d.v == a.mineral) d.v = "un";
                            else d.v = a.mineral;
                            d3.select(this)
                                .attr("fill", getColor)
                                .attr("fill-opacity", fillOpacity);
                        })
                        .on("mouseover", function(d,i) {
                            if (d3.event.shiftKey) {
                                d.v = a.mineral;
                                d3.select(this)
                                    .attr("fill", getColor)
                                    .attr("fill-opacity", fillOpacity);
                            }
                        });


                var reset = function() {
                    var bottomLeft = project([bounds.left,bounds.bottom]),
                    topRight = project([bounds.right,bounds.top]);
                    svg.attr("width", topRight[0]-bottomLeft[0])
                        .attr("height", bottomLeft[1] - topRight[1])
                        .style("margin-left", bottomLeft[0] + "px")
                        .style("margin-top", topRight[1] + "px");
                    //g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");
                }
                reset();
                a.map.events.register("moveend", a.map, reset);
                a.svg = svg;
            }
            this.map.addLayer(overlay);
            this.overlay = overlay;

        },
        onChangeOpacity: function(opacity){
            this.svg.attr("opacity",opacity);
        },
        setDraw: function(bool){
            if (bool === typeof('undefined')) bool = true;
            if (bool == true) {
                this.svg.attr("pointer-events","all");
            } else {
                this.svg.attr("pointer-events","none");
            }
        },
        onChangeMineral: function(mineral){
            this.mineral = mineral
        },
        getData: function(){
            return this.data;
        }
    });
    return ClassifyMap;
});
