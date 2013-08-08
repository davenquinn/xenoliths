define([
    "backbone",
    "d3", 
    "views/map/base", 
    "options"
    ],function(Backbone, d3, MapBase, Options){

    Map = MapBase.extend({
        initialize: function(){
            Map.__super__.initialize.apply(this, arguments);
            this.data = this.options.data
            this.setupEventHandlers();
            this.colormap = new this.colors["oxide_total"]();
            this.addPoints(this.data);
        },
        addPoints: function(data){
            var a = this;
            this.overlay = new OpenLayers.Layer.Vector("measurements");

            // Add the container when the overlay is added to the map.
            //this.overlay.afterAdd = this.drawSVG;
            this.map.addLayer(this.overlay);
            this.drawSVG();
        },
        drawSVG: function(){
            var a = this;
            var project = function(x) {
                var point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]));
                return [point.x, point.y];
            }
            var div = d3.selectAll("#" + a.overlay.div.id);
            div.selectAll("svg").remove();
            var svg = div.append("svg")
                //.attr("width", $("#map").width())
                //.attr("height", $("#map").height());

            var g = svg.append("svg:g");
            
            var bounds = a.getBounds(a.data)
            var path = d3.geo.path().projection(project);
            //var ramp=d3.scale.sqrt().domain([0,10]).range(["#71eeb8","salmon"]);

            a.feature = g.selectAll(".dot")
                .data(a.data.features)
                .enter().append("path")
                    .attr("class", "dot")
                    .attr("d",path.pointRadius(3))
                    .style("fill", a.colormap.func)
                    .on("mouseover", a.onMouseMove)

            var reset = function() {
                var bottomLeft = project(bounds[0]),
                topRight = project(bounds[1]);

                svg.attr("width", topRight[0]-bottomLeft[0])
                    .attr("height", bottomLeft[1] - topRight[1])
                    .style("margin-left", bottomLeft[0] + "px")
                    .style("margin-top", topRight[1] + "px");

                g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");

                a.feature.attr("d", path);
            }
            reset();
            a.map.events.register("moveend", a.map, reset);
        },
        getBounds: function(data){
            xvalues = [];
            yvalues = [];
            $.each(data.features, function(i,el){
                c = el.geometry.coordinates;
                xvalues.push(c[0]);
                yvalues.push(c[1]);
            });
            return [[Math.min.apply(null,xvalues),Math.min.apply(null,yvalues)],
                    [Math.max.apply(null,xvalues),Math.max.apply(null,yvalues)]];
        },
        setupEventHandlers: function(){
            var a = this;
            this.dispatcher = d3.dispatch("updated");
            this.onMouseMove = function(d,i) {
                d3.select(".dot.selected")
                    .attr("class","dot")
                d3.select(this)
                    .attr("class","dot selected")
                a.dispatcher.updated(d);
            }
        },
        setColormap: function(name, options){
            this.colormap = new this.colors[name](options);
            this.drawSVG();
        }
    });
    return Map;
});
