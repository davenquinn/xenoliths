//var po = org.polymaps;

var Point = Class.$extend({
	__init__: function(x, y){
		this.x = x;
		this.y = y;
	}
});

var Bounds = Class.$extend({
	__init__: function(left, bottom, right, top){
		this.left = left;
		this.right = right;
		this.bottom = bottom;
		this.top = top;
	},
	getCenter: function(){
		x = (this.left + this.right)/2.0;
		y = (this.top + this.bottom)/2.0;
		return Point(x,y);
	}
});

var DataView = Class.$extend({
	__classvars__: {
	},
	__init__: function(div, data){
		var a = this;
		this.oxides = ["SiO2","MgO","FeO","CaO","Al2O3","Cr2O3","TiO2","NiO","MnO","Na2O"]

		width = $(div).width();

		this.parent = d3.select(div)
			.append("div")
			.attr("class","selected")

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
		this.id = this.center.append("text")
			.attr("class", "label")
			.attr("x", 0)
			.attr("y", 4)
			.style("text-anchor", "middle")
			.style("alignment-baseline", "middle")
			.style("font-size", "2.5em")
		this.sample = this.center.append("text")
			.attr("class", "sample")
			.attr("x", 0)
			.attr("y", "-1.8em")
			.style("text-anchor", "middle")
			.style("alignment-baseline", "middle")
			.style("font-size", "1.2em")
		this.total = this.center.append("text")
			.attr("class", "total")
			.attr("x", 5)
			.attr("y", "1.9em")
			.style("text-anchor", "middle")
			.style("alignment-baseline", "middle")
			.style("font-size", "1.2em")

		this.overlay = this.center.append("g")
		this.overlay.append("circle")
			.attr("r", this.r-100-2)
			.attr("stroke-width",5)
			.style("fill", "white")
		this.overlay_name = this.overlay.append("text")
			.attr("class", "label")
			.attr("x", 0)
			.attr("y", 4)
			.style("text-anchor", "middle")
			.style("alignment-baseline", "middle")
			.style("font-size", "1.8em")
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
    	this.arc = d3.svg.arc().innerRadius(this.r - 100).outerRadius(this.r)


    	this.arcTween = function(s) {
  			var i = d3.interpolate(this._current, s);
  			this._current = i(0);
  			return function(t) {return a.arc(i(t));};
  		};

    	this.onMouseMove = function(d,i){
    		el = d3.select(this);
    		b = el.attr("fill");
    		a.overlay.style("display","inherit")
				.select("circle")
    				.style("stroke", b)

    		a.overlay_name.text(el.attr("class"))
    		a.overlay_val.text(d.value.toFixed(2)+"%")
    		//el.attr("stroke", b);
    		//el.attr("stroke-width", 10)
    		console.log(this);
    		console.log(d);
    	}
    	this.onMouseOut = function(d,i){
     		a.overlay.style("display","none")   		
    	}

  		this.arcs = this.svg.selectAll("path")
    		.data(this.processData(data))
  			.enter().append("svg:path")
    			.attr("fill", function(d, i) { return a.color(i); })
    			.attr("class", function(d,i) { return a.oxides.concat(["?"])[i]; })
    			.attr("d", this.arc)
    			.on("mouseover", this.onMouseMove)
    			.on("mouseout", this.onMouseOut)
    			.each(function(d) { this._current = d; })
	},
	processData: function(data){
		oxides = data.properties.oxides;
		ob = [];
		for (var key in this.oxides) { v = this.oxides[key]; ob.push(oxides[v]);}
		if (oxides.total < 100) ob.push(100-oxides.total);
		else ob.push(0);
		d = this.donut(ob);
		return d
	},
	update: function(data){
		var a = this;
		this.id.text(data.id);
		this.sample.text(data.properties.sample);
		this.total.text(data.properties.oxides.total.toFixed(2)+"%")
  		this.arcs = this.arcs.data(this.processData(data));
  		this.arcs.transition().duration(300).attrTween("d", a.arcTween); // redraw the arcs
  	}
});

