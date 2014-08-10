var _ = require('underscore');
var Backbone = require('backbone');
var d3 = require('d3');
var GenericView = require('../base/generic');
var Options = require('../../options');
var Colorizer = require('../base/colors');


TernaryChart = GenericView.extend({
defaults: {
    margin: {
        left: 50,
        top: 20,
        bottom: 40,
        right: 0
    },
    system: "pyroxene",
    selection: [],
},
initialize: function(){
    _.defaults(this.options, this.defaults)
    console.log(this.options)
    this.parent = this.options.parent;
    this.data = this.options.data;
    this.sel = this.options.selection;
    this.options.colormap = new Colorizer["samples"]();
    m = this.options.margin
    this.width = this.$el.width()-m.left-m.right;
    this.height = this.$el.height()-m.top-m.bottom;
    this.system = Options.systems[this.options.system]

    this.setupEventHandlers();
    this.loadAxes();
},
loadAxes: function(){
    var a = this;

    this.drawSVG()
},
drawSVG: function(){
    var a = this;
    this.svg = d3.select(this.el).append("svg")
            .attr("width", this.$el.width())
            .attr("height", this.$el.height())
            .append("g")
                .attr("transform", "translate(" + m.left + "," + m.top + ")")
    var sin30 = Math.pow(3,1/2)/2;
    var cos30 = .5;
    var rad = this.height/1.5;
    var h = this.height
    var c = [this.width/2,rad];
    var l = [c[0]-rad*sin30, c[1] + rad*cos30];
    var r = [c[0]+rad*sin30, c[1] + rad*cos30];
    var t = [c[0], c[1] - rad];

    var corners = [t,r,l];
    this.x = function(s){
        d = a.system.components.map(function(i){return s[i]});
        return corners[0][0] * d[0] + corners[1][0] * d[1] + corners[2][0] * d[2]
    };
    this.y = function(s){
        d = a.system.components.map(function(i){return s[i]});
       return corners[0][1] * d[0] + corners[1][1] * d[1] + corners[2][1] * d[2]
    };
    var points = corners.reduce(function(p,c){
      return p+" "+c[0]+","+c[1];
    });
    this.svg.append('polygon')
          .attr('stroke', 'black')
          .attr('fill','white')
          .attr('points', points)


    this.points = this.svg.append("g")
        .attr("class","data")

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
    console.log(a.options.system)
    this.xTransform = function(d) { return a.x(d.properties.systems[a.options.system]); }
    this.yTransform = function(d) { return a.y(d.properties.systems[a.options.system]); }
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
            .style("fill", a.options.colormap.func);   
    };
},
setColormap: function(name, options){
    this.options.colormap = new Colorizer[name](options);
    this.points.selectAll(".dot").style("fill", this.options.colormap.func)
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
module.exports = TernaryChart;


