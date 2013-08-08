
// Store the currently-displayed angles in this._current.
// Then, interpolate from this._current to the new angles.

var Chart = Class.$extend({
	__classvars__: {

	},
	__init__: function(div, axes, data){
		this.colors = { "CK-2": "lightblue",
			"CK-3": "lightgreen",
			"CK-4": "coral" }
		var a = this;
		this.div = div;
		this.axes = axes;
		this.data = data.features;

		margin = {
			left: 50,
			top: 20,
			bottom: 40,
			right: 0
		}
		var width = $(div).width()-margin.left-margin.right;
		var height = $(div).height()-margin.top-margin.bottom;

		var x = d3.scale.linear()
				.domain([-.05, 1.05*d3.max(this.data,function(d) { return d.properties.oxides[a.axes.x];})])
				.range([0, width]);
		var y = d3.scale.linear()
				.domain([-.05,1.05*d3.max(this.data,function(d) { return d.properties.oxides[a.axes.y];})])
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

		this.svg = d3.select(div).append("svg")
	    		.attr("width", $(div).width())
	    		.attr("height", $(div).width())
	  			.append("g")
	    			.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
	    			.call(this.zoomer);

		this.svg.append("rect")
			.attr("id", "clip")
		    .attr("width", width)
		    .attr("height", height);

		this.svg.append("g")
		    .attr("class", "x axis")
		    .attr("transform", "translate(0," + height + ")")
		    .call(this.xAxis)
			.append("text")
				.attr("class", "label")
				.attr("x", width/2)
				.attr("y", 30)
				.style("text-anchor", "center")
				.text(this.axes.x+" (%)");

		this.svg.append("g")
		    .attr("class", "y axis")
		    .call(this.yAxis)
		    .append("text")
		      .attr("class", "label")
		      .attr("transform", "rotate(-90)")
		      .attr("y", -40)
		      .attr("x", -height/2)
		      .attr("dy", ".71em")
		      .style("text-anchor", "center")
		      .text(this.axes.y + " (%)")


	    var clip = this.svg.append("defs").append("svg:clipPath")
	        .attr("id", "clip")
	        .append("svg:rect")
	        .attr("id", "clip-rect")
	        .attr("x", "0")
	        .attr("y", "0")
	        .attr("width", width)
	        .attr("height", height)

		 var points = this.svg.append("g")
		 	.attr("class","data")
		 	.attr("clip-path", "url(#clip)");

		 
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
		this.xTransform = function(d) { return a.x(d.properties.oxides[a.axes.x]); }
		this.yTransform = function(d) { return a.y(d.properties.oxides[a.axes.y]); }
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
    $("#content").height($(window).height()-$("#header").outerHeight());

	chart = Chart("#chart", config.axes, data);
	chart.events.on("updated",function(d){
		if (typeof dataView === "undefined") window.dataView = DataView("#data", d);
		else window.dataView.update(d);
	});

	$("#data h1").subscriptify();
});