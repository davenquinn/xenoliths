var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var Si = d3.scale.linear()
    .range([0, 400])
    .domain([0,1])

var Fe = d3.scale.linear()
    .range([0, 400]);
    .domain([0,1])

var color = d3.scale.linear()
    .domain([0,40,50])
    .range(["black", "gray", "red"]);

//var color = d3.scale.category10();

var SiAxis = d3.svg.axis()
    .scale(Si)
    .attr("transform", "rotate(90)");

var FeAxis = d3.svg.axis()
    .scale(Fe)
    .attr("transform", "rotate(-30)");

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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
      .attr("cx", function(d) { return Si(d.major.SiO2); })
      .attr("cy", function(d) { return Fe(d.major.FeO); })
      .style("fill", function(d) { return color(d.oxides.SiO2); });

  var legend = svg.selectAll(".legend")
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
      .text(function(d) { return d; });

});
