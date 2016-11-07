// By Alex Krusz at Velir

//Width and height
var w = 800;
var h = 550;
var barPadding = 20;
var bottomMargin = 42;
var leftMargin = 40;
var startingX = 5;
var xStep = 1;
var verticalDataPixels = h - bottomMargin;
var minDisplayValue = Infinity;
var maxDisplayValue = -Infinity;

mainData = {"config":{"pressure":{"s":0.2,"v":1.5}},"samples":[{"core":{"T":956.1560232303294,"errors":{"Total":62.012290524826795,"pressure":6.460002199272697,"probe":1.1729627402516776,"th":61.663738989221976}},"id":"CK-5","rim":{"T":964.1776480192347,"errors":{"Total":62.63267335799047,"pressure":6.502155831321045,"probe":1.641748862733479,"th":62.27261358081626}}},{"core":{"T":1062.0711941489894,"errors":{"Total":71.32327543975953,"pressure":7.016586340358201,"probe":0.9480873913334884,"th":70.97096776769001}},"id":"CK-6","rim":{"T":1068.9329022084594,"errors":{"Total":71.9232636526873,"pressure":7.052644610892384,"probe":1.1058745932893081,"th":71.56810113332848}}},{"core":{"T":981.2565468759313,"errors":{"Total":64.17090253375969,"pressure":6.59190543157558,"probe":1.090928655649935,"th":63.82210737234185}},"id":"CK-7","rim":{"T":999.5325977999374,"errors":{"Total":65.62823649896119,"pressure":6.6879460650159475,"probe":1.2395213936117522,"th":65.2748067029677}}},{"core":{"T":1038.2073753501559,"errors":{"Total":68.46410178659578,"pressure":6.8911819910665475,"probe":0.8533226750688875,"th":68.11106139698283}},"id":"CK-4","rim":{"T":1049.0710946258691,"errors":{"Total":69.38160475569174,"pressure":6.9482708274402345,"probe":0.8957619139255415,"th":69.02699632446087}}},{"core":{"T":953.4419014353651,"errors":{"Total":61.870148189536394,"pressure":6.445739491343804,"probe":1.6385579274124136,"th":61.511647737021626}},"id":"CK-2","rim":{"T":956.3006888750143,"errors":{"Total":62.02830141038731,"pressure":6.46076241712339,"probe":0.873030022297189,"th":61.684735092464415}}},{"core":{"T":1040.8455491081445,"errors":{"Total":68.83086757506545,"pressure":6.905045592119997,"probe":0.7601923924291543,"th":68.47941868936559}},"id":"CK-3","rim":{"T":1054.4426788980113,"errors":{"Total":70.03246237339532,"pressure":6.97649849862697,"probe":0.7176520370353472,"th":69.68040779396622}}}]};

generateGraph();

function generateGraph(){
	
	var isUserData = false;
	
	samples = mainData.samples.sort(function(a,b){
		return a.core.T-b.core.T;
	})

	var data = samples.map(function(x){
		return x.core.T;
	});
	var stdDevs = samples.map(function(x){
		return x.core.errors.Total;
	});

	var distribution = new normalDistribution();
	
	// We'll choose between "dot", "bar", and "line".
	// Line will take some more SVG/CSS wizardry to implement properly.
	var graphType = "dot";
	var displayDistribution = distribution;
	var distroType = "normal";
	
	var keepScale = false;
	var startFromZero = false;
	
	if(maxDisplayValue === -Infinity || !keepScale) {
		maxDisplayValue = -Infinity;
		minDisplayValue = Infinity;
		
		for(i = 0; i < data.length; i++){
			if(data[i] + (displayDistribution.endX - distribution.mean)
			/distribution.standardDeviation*stdDevs[i] > maxDisplayValue){
				maxDisplayValue = data[i] + (displayDistribution.endX - distribution.mean)
					/distribution.standardDeviation*stdDevs[i];
			}
			if(data[i] + (displayDistribution.startX - distribution.mean)
			/distribution.standardDeviation*stdDevs[i] < minDisplayValue){
				minDisplayValue = data[i] + (displayDistribution.startX - distribution.mean)
				/distribution.standardDeviation*stdDevs[i];
			}
		}
		// If startFromZero and the graph doesn't span the x-axis,
		// we'll make either the top or bottom of the graph 0.
		if(startFromZero){
			if(minDisplayValue > 0){
				minDisplayValue = 0;
			}
			else if(maxDisplayValue < 0){
				maxDisplayValue = 0;
			}
		}
	}
	
	// This is the vertical size of the display area, in terms of data value.
	var dataRange = maxDisplayValue - minDisplayValue;
	var maxValue = Math.max.apply(Math, data);
	var minValue = Math.min.apply(Math, data);
	
	// Set up scales
	var yScale = d3.scale.linear()
		.domain([minDisplayValue, maxDisplayValue])
		.range([verticalDataPixels, 0]);
	
	// Define the Y axis
	// TODO: make the X-axis this way
	var yAxis = d3.svg.axis()
					.scale(yScale)
					.tickSize(-w + leftMargin, 0)
					.orient("left")
					.ticks(20);
	
	// This is so we can scale the opacity down for data points with large
	// standard deviations, so total color mass is the same for each data point.
	// In the case that the difference in magnitude between the lowest and
	// highest stddevs is large, this will cause the large bands to be too pale.
	// So, we calculate a minimum stddev for the purposes of normalizing opacity.
	var minOpacity = 0.2;
	var minStdDev = Math.max.apply(Math, stdDevs)/Math.min.apply(Math, stdDevs) > 1.0/minOpacity
					? Math.max.apply(Math, stdDevs) * minOpacity
					: Math.min.apply(Math, stdDevs);
	
	//Create SVG element
	var svg = d3.select("body")
				.append("svg")
				.attr("class","graph")
				.attr("width", w)
				.attr("height", h);

	var distributionGradient = svg.append("svg:defs")
	  .append("svg:linearGradient")
		.attr("id", "distribution")
		.attr("x1", "0%")
		.attr("y1", "100%")
		.attr("x2", "0%")
		.attr("y2", "0%")
		.attr("spreadMethod", "pad");

	var subGradients = 100;
	var showBands = false;
	var numBands = 10;

	var xValues = [];
	var densityValues = [];
	
	for(i = 0; i <= subGradients; i++){
		xValues[i] = displayDistribution.startX + displayDistribution.widthInSDs()
						* distribution.standardDeviation* i / subGradients;
		densityValues[i] = displayDistribution.value(xValues[i]);
	}
	var densityMax = Math.max.apply(Math, densityValues);
	
	var barColor = "#049";
	var epsilon = 1 / (2 * numBands);
	for(i = 0; i <= subGradients; i++){
		// TODO: Implement Ramer–Douglas–Peucker algorithm for more efficient interpolation
		// of density function when implementing separate gradients for each data point.
		var opacity = (graphType == "bar")
			? 1 - densityValues[i] / densityMax
			: densityValues[i] / densityMax;
			
		if(showBands){
			if(opacity < epsilon){
				opacity = 0;
			}
			opacity = Math.ceil(numBands * (opacity - epsilon)) / numBands;
		}
		
		distributionGradient.append("svg:stop")
		.attr("offset", (100 / subGradients) * i + "%")
		.attr("stop-color", barColor)
		.attr("stop-opacity", opacity);
	}
	
	// To look decent, bars must be at least one full pixel for uniform distro,
	// three pixels for others. Due to sampling only one point, single-px nonuniform
	// bars can disappear.
	var minHeight = (distroType == "uniform") ? 1 : 3;
	
	//Create Y axis
	svg.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(40,0)")
		.call(yAxis);

	// Make the data bars
	svg.selectAll("rect.graph_gradient")
	   .data(samples)
	   .enter()   
		   .append("rect")
		   .attr("class","graph_gradient")
		   .attr("x", function(d, i) {
				return leftMargin + i * ((w - leftMargin)/ samples.length);
		   })
		   .attr("y", function(d, i) {
				// two basic behaviors: scaling or translating
				return verticalPositionOfDatum(
					d.core.T + (displayDistribution.endX - distribution.mean)/distribution.standardDeviation*d.core.errors.Total,
					minDisplayValue, maxDisplayValue, verticalDataPixels);
			})
		   .attr("width", (w - leftMargin) / samples.length - barPadding)
		   .attr("height", function(d, i) {
				var top = undefined;
				var bottom = undefined;

				top = verticalPositionOfDatum(d.core.T + displayDistribution.widthInSDs()*d.core.errors.Total,
							minDisplayValue, maxDisplayValue, verticalDataPixels);
				bottom = verticalPositionOfDatum(d.core.T, minDisplayValue, maxDisplayValue, verticalDataPixels);
			
				return (bottom - top < minHeight) ? minHeight : bottom - top;
			})
			.style("fill", "url(#distribution)")
			.style("opacity", function(d, i) {
				return Math.min(1, minStdDev / d.core.errors.Total);
			});
	
	
	// Make a background white box under the text.
	svg.append("rect")
		.attr("class", "background")
		.attr("x", leftMargin + 1)
		.attr("y", verticalDataPixels + 1)
		.attr("width", w - leftMargin)
		.attr("height", h - verticalDataPixels - 1);
	
	// Put in the text for the x-axis labels.
	svg.selectAll("text.x-scale")
	   .data(samples)
	   .enter()
	   .append("text")
	   .attr("class", "x-scale")
	   .text(function(d, i) {
			return d.id;
	   })
	   .attr("text-anchor", "middle")
	   .attr("x", function(d, i) {
			return leftMargin + i * ((w - leftMargin) / samples.length) + ((w - leftMargin) / samples.length - barPadding) / 2;
	   })
	   .attr("y", function(d) {
			return h - 30;
	   })
	   .attr("font-family", "sans-serif")
	   .attr("font-size", "11px")
	   .attr("fill", "black");
	   
	svg.selectAll("text.x-scale")
		.append('tspan')
		.attr("class", "stats")
		.attr("x", function(d, i) {
			return leftMargin + i * ((w - leftMargin) / samples.length) + ((w - leftMargin) / samples.length - barPadding) / 2;
		})
		.attr("y", function(d, i) {
			return h - 10;
		})
		.attr("fill", "#888888")
		.text(function(d, i) {
			return "σ: " + d.core.errors.Total.toFixed(1);
		})
		.append('tspan')
		.attr("x", function(d, i) {
			return leftMargin + i * ((w - leftMargin) / samples.length) + ((w - leftMargin) / samples.length - barPadding) / 2;
		})
		.attr("y", function(d, i) {
			return h - 20;
		})
		.text(function(d) {
			return "μ: " + d.core.T.toFixed(0);
		});
}

function verticalPositionOfDatum(dataValue, windowMin, windowMax, verticalPixels){
	return verticalPixels * (windowMax - dataValue) / (windowMax - windowMin);
}

function erf(x){
	var sign = (x < 0) ? -1 : 1;
	x = Math.abs(x);
	
	var a1 =  0.254829592;
	var a2 = -0.284496736;
	var a3 =  1.421413741;
	var a4 = -1.453152027;
	var a5 =  1.061405429;
	var p  =  0.3275911;
	
	var t = 1.0/(1.0 + p*x);
	var y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*Math.exp(-x*x);
	return sign*y;
}

function sech(x){
	return 2 / (Math.exp(x) + Math.exp(-x));
}
