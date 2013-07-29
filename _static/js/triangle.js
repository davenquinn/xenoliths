var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = $(window).width() - margin.left - margin.right,
    height = $(window).height() - margin.top - margin.bottom;

var Point = Class.$extend({
  __init__: function(x, y){
    this.x = x;
    this.y = y;
  },
  asString: function(){
    return this.x+","+this.y;
  }
});

var color = d3.scale.linear()
    .domain([0,40,50])
    .range(["black", "gray", "red"]);

var sin30 = Math.pow(3,1/2)/2;
var cos30 = .5;

//var color = d3.scale.category10();
var rad = height/1.5;
var h = 1.5*rad
var c = Point(width/2,rad);
var l = Point(c.x-rad*sin30, c.y + rad*cos30);
var r = Point(c.x+rad*sin30, c.y + rad*cos30);
var t = Point(c.x, c.y - rad);

var Si = d3.scale.linear()
    .domain([0,1])
    .range([0, h]);

var Fe = d3.scale.linear()
    .domain([0,1])
    .range([0, h]);

var SiAxis = d3.svg.axis()
    .scale(Si)
    .orient("left")

var FeAxis = d3.svg.axis()
    .scale(Fe)
    .orient("bottom")

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    
  svg.append('polygon')
      .attr('stroke', 'black')
      .attr('fill','white')
      .attr('points', t.asString()+' '+l.asString()+' '+r.asString())

d3.json('/data/CK-2_compositions.json', function(data) {

  //Si.domain(d3.extent(data, function(d) { return d.major.SiO2; })).nice();
  //Fe.domain(d3.extent(data, function(d) { return d.major.FeO; })).nice();

  /*svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(SiAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("SiO2");

  svg.append("g")
      .attr("class", "y axis")
      .call(FeAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("FeO")*/

  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", function(d) { return r.x - rad - sin30*Fe(d.major.FeO) + cos30*Si(d.major.SiO2); })
      .attr("cy", function(d) { return t.y + h - Si(d.major.SiO2); })
      .style("fill", function(d) { return color(d.oxides.SiO2); });



  /*var legend = svg.selectAll(".legend")
      .data(color.domain())
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });*/

});
