var $ = require('jquery');
var GenericView = require('../base/generic');
var d3 = require('d3');
var Options = require('../../options');


OxidesWheel = GenericView.extend({
    initialize: function(options){
        this.options = options;
        var a = this;
        this.oxides = Options.oxides
        this.createEventHandlers()

    },
    render: function(data) {
        var a = this;

        width = $("#tabs").innerWidth();
        this.parent = d3.select(this.el)
        this.r = width/2
        this.svg = this.parent.append("svg")
            .attr("width", width)
            .attr("height", width)
            .attr("viewBox", "0 0 "+width+" "+width)
            .attr("preserveAspectRatio", "xMidYMid")
            .append("g")
                .attr("transform", "translate(" + this.r + "," + this.r + ")");
        this.center = this.svg.append("g")
            .attr("class","center")

        this.center.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", -22)
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .style("font-size", "1em")
            .style("font-weight","600")
            .style("fill ", "#888")
            .text("OXIDES")

        this.mineral = this.center.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 28)
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .style("font-size", ".8em")
            .style("font-weight","600")

        this.total = this.center.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 4)
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .style("font-size", "1.8em")

        this.overlay = this.center.append("g")
        this.overlay.append("circle")
            .attr("r", this.r-85-2)
            .attr("stroke-width",5)
            .style("fill", "white")
        this.overlay_name = this.overlay.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 4)
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .style("font-size", "1.9em")
        this.overlay_val = this.overlay.append("text")
            .attr("class", "total")
            .attr("x", 5)
            .attr("y", "1.9em")
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .style("font-size", "1.2em")
        this.overlay.style("display", "none");

        this.color = d3.scale.category20(),
        this.donut = d3.layout.pie().sort(null)
        this.arc = d3.svg.arc().innerRadius(this.r - 85).outerRadius(this.r)

        this.arcs = this.svg.selectAll("path")
            .data(this.processData(data))
            .enter().append("svg:path")
                .attr("pointer-events","all")
                .attr("fill", function(d, i) { return a.color(i); })
                .attr("class", function(d,i) { return a.oxides.concat(["?"])[i]; })
                .attr("d", this.arc)
                .on("mouseover", this.onMouseIn)
                .on("mouseout", this.onMouseOut)
                .each(function(d) { this._current = d; })
    },
    createEventHandlers: function(){
        var a = this;
        this.update = function(data){
            if (typeof this.total === "undefined") this.render(data);
            else {
                var a = this;
                this.arcs = this.arcs.data(this.processData(data));
                this.arcs.transition().duration(300).attrTween("d", a.arcTween); // redraw the arcs
            }
            this.total.text(data.properties.oxides.Total.toFixed(2)+"%")
            min = Options.minerals[data.properties.mineral];
            this.mineral.text(min.name.toUpperCase());
            color = d3.hsl(min.color);
            color.l = .3
            this.mineral.style("fill",color.toString());

        }
        this.arcTween = function(s) {
            var i = d3.interpolate(this._current, s);
            this._current = i(0);
            return function(t) {return a.arc(i(t));};
        };

        this.onMouseIn = function(d,i){
            el = d3.select(this);
            b = el.attr("fill");
            a.overlay.style("display","inherit")
                .select("circle")
                    .style("stroke", b)

            a.overlay_name.text(el.attr("class"))
            a.overlay_val.text(d.value.toFixed(2)+"%")
            //el.attr("stroke", b);
            //el.attr("stroke-width", 10)
        }
        this.onMouseOut = function(d,i){
            a.overlay.style("display","none")
        }
    },
    processData: function(data){
        oxides = data.properties.oxides;
        ob = [];
        for (var key in this.oxides) { v = this.oxides[key]; ob.push(oxides[v]);}
        if (oxides.Total < 100) ob.push(100-oxides.Total);
        else ob.push(0);
        d = this.donut(ob);
        return d
    }
});
module.exports = OxidesWheel;
