var Backbone = require('backbone');
var d3 = require('d3');
var MapBase = require('./base');
var Options = require('../../options');


Map = MapBase.extend({
    initialize: function(){
        Map.__super__.initialize.apply(this, arguments);
        this.parent = this.options.parent;
        this.data = this.options.data;
        this.sel = this.options.selected;
        if (!this.sel) this.sel = [];

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
        this.svg = div.append("svg")
            .on("click", this.onBackgroundClick);

            //.attr("width", $("#map").width())
            //.attr("height", $("#map").height());

        var g = this.svg.append("svg:g")
        
        var bounds = a.getBounds(a.data)
        var path = d3.geo.path().projection(project);
        //var ramp=d3.scale.sqrt().domain([0,10]).range(["#71eeb8","salmon"]);

        a.feature = g.selectAll(".dot")
            .data(a.data.features)
            .enter().append("path")
                .attr("class", "dot")
                .attr("d",path.pointRadius(3.5))
                .style("fill", a.colormap.func)
                .on("mouseover", a.onMouseMove)
                .on("mouseout", a.onMouseOut)
                .on("click",a.onClick)
                .classed("selected", function(d){ return a.sel.indexOf(d) != -1 });

        var reset = function() {
            var bottomLeft = project(bounds[0]),
            topRight = project(bounds[1]);

            a.svg.attr("width", topRight[0]-bottomLeft[0])
                .attr("height", bottomLeft[1] - topRight[1])
                .style("margin-left", bottomLeft[0] + "px")
                .style("margin-top", topRight[1] + "px");

            g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");

            a.feature.attr("d", path);
        }
        reset();
        a.map.events.register("moveend", a.map, reset);
        if (this.sel[0] != null) {
            a.zoomToPoint(this.sel[0].geometry.coordinates, 4)
        }
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
            //if (a.selectMode == "multiple") {
                toSelect = !item.classed("selected")
                item.classed("selected", toSelect)
                if (toSelect) {
                    a.sel.push(d)
                } else {
                    var index = a.sel.indexOf(d);
                    a.sel.splice(index,1);
                }
                a.dispatcher.updated.apply(this,arguments);
            //}
            d3.event.stopPropagation();
        };
        this.onBackgroundClick = function(d,i){
            //if (a.selectMode == "multiple") {
                d3.selectAll(".dot.selected").classed("selected",false);
                d3.event.stopPropagation();
                a.sel.length = 0;
                a.dispatcher.updated.apply(this,arguments);
            //}
        };
    },
    setColormap: function(name, options){
        this.colormap = new this.colors[name](options);
        this.drawSVG();
    },
    setSelectMode: function(mode){
        this.selectMode = mode;
    }
});
module.exports = Map;

