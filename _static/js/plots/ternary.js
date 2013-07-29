var sin30 = Math.pow(3,1/2)/2;
var cos30 = .5;

// Store the currently-displayed angles in this._current.
// Then, interpolate from this._current to the new angles.

var Point = Class.$extend({
  __init__: function(x, y){
    this.x = x;
    this.y = y;
  },
  asString: function(){
    return this.x+","+this.y;
  }
});

var Ternary = Class.$extend({
	__init__: function(div, axes, data){
		this.colors = { "CK-2": "lightblue",
			"CK-3": "lightgreen",
			"CK-4": "coral" }
		var a = this;
		this.div = div;
		this.axes = axes;
		this.data = data.features;

		margin = {
			left: 60,
			top: 40,
			bottom: 40,
			right: 0
		}
		var width = $(div).width()-margin.left-margin.right;
		var height = $(div).height()-margin.top-margin.bottom;

		var rad = height/1.5;
		var h = height
		var c = Point(width/2,rad);
		var l = Point(c.x-rad*sin30, c.y + rad*cos30);
		var r = Point(c.x+rad*sin30, c.y + rad*cos30);
		var t = Point(c.x, c.y - rad);

		var x = d3.scale.linear()
				.domain([0,1])
				.range([0, width]);
		var y = d3.scale.linear()
				.domain([0,1])
				.range([height, 0]);

		this.x = x; this.y = y

		this.setupEventHandlers();

		this.xAxis = d3.svg.axis()
		    .scale(x)
		    .orient("bottom")
		    .tickSize(-height);

		this.yAxis = d3.svg.axis()
		    .scale(y)
		    .orient("left")
		    .ticks(5)
		    .tickSize(-width)

		this.zoomer = d3.behavior.zoom()
			.x(x).y(y)
			.scaleExtent([1, 40])
			.on("zoom", this.onZoom);

		this.xTransform = function(d) {
			sy = d.properties.transforms.pyroxene
			return r.x - rad - sin30*x(sy.Fs) + cos30*y(sy.En);
		};
		this.yTransform = function(d) { return t.y + h - y(d.properties.transforms.pyroxene.En); }

		this.svg = d3.select(div).append("svg")
	    		.attr("width", $(div).width())
	    		.attr("height", $(div).width())
	  			.append("g")
	    			.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
	    			.call(this.zoomer);
    
		this.svg.append('polygon')
		      .attr('stroke', 'black')
		      .attr('fill','white')
		      .attr('points', t.asString()+' '+l.asString()+' '+r.asString())

		 var points = this.svg.append("g")
		 	.attr("class","data")
		 
		 points.selectAll(".dot")
		    .data(this.data)
		    .enter().append("circle")
				.attr("class", "dot")
				.attr("r", 3.5)
				.attr("cx", this.xTransform)
				.attr("cy", this.yTransform)
				.on("mouseover", this.onMouseMove)
				.attr("style", function(d) {
					return "fill: " + a.colors[d.properties.sample]; 
				});

		this.dims = [width, height]
	},
	setupEventHandlers: function(){
		var a = this;
		this.events = d3.dispatch("updated");
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
		this.onMouseMove = function(d,i) {
			d3.select(".dot.selected")
				.attr("class","dot")
			d3.select(this)
				.attr("class","dot selected")
			a.events.updated(d);
		}
	},

});


var chart, dataView;
jQuery(document).ready(function($){

  	$.fn.subscriptify = function() {
    	return this.each(function() {
    		ntext = $(this).text().replace(/(\d+)/g, '<sub>$1</sub>');
    		$(this).html(ntext);
    	});
    };

	chart = Ternary("#chart", config.axes, data);
	chart.events.on("updated",function(d){
		if (typeof dataView === "undefined") window.dataView = DataView("#data", d);
		else window.dataView.update(d);
	});

	$("#data h1").subscriptify();
});