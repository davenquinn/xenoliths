var map;
var mapMinZoom = 0;
var mapMaxZoom = 8;
var emptyTileURL = "http://www.maptiler.org/img/none.png";
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;

var dataPane;

var SelectFeaturesControl = OpenLayers.Class(OpenLayers.Control.SelectFeature, {
    initialize: function(lyr) {
        console.log(lyr);
        options = {
            clickout: false,
            toggle: false,
            multiple: false,
            hover: false,
            toggleKey: "ctrlKey", // ctrl key removes from selection
            multipleKey: "shiftKey", // shift key adds to selection
            box: true
        };
        // Call the super constructor, you will have to define the variables geometry, attributes and style
        OpenLayers.Control.SelectFeature.prototype.initialize.apply(this, [lyr, options]);
        this.bind();
    },
    bind: function(){
        control = this;
        $("input:radio[name=mode]").change(function(evt){
            val = $(this).val();
            if (val == "select") control.activate();
            if (val == "navigate") control.deactivate();
        });
    },
    CLASS_NAME: "SelectFeaturesControl"
});

var Map = Class.$extend({
    __init__: function(div, options){
        this.options = options;
        this.sample = options.sample;
        this.bounds = OpenLayers.Bounds.fromArray(options.bounds);

        var mapOptions = {
            div: div,
            controls: [],
            maxExtent: this.bounds,
            restrictedExtent: this.bounds,
            maxResolution: 64.000000,
            numZoomLevels: 8
        };
        this.map = new OpenLayers.Map(mapOptions);
        this.GeoJSON = new OpenLayers.Format.GeoJSON();

        this.map.addControls([new OpenLayers.Control.Zoom(),
                 new OpenLayers.Control.Navigation(),
                 new OpenLayers.Control.MousePosition({numDigits:2}),
                 new OpenLayers.Control.ArgParser()]);

        this.setupEventHandlers();
        this.setupTiles();
        this.map.zoomToExtent(this.bounds);

    },
    setupTiles: function(){
        var a = this;
        var getURL = function(bounds) {
            bounds = this.adjustBounds(bounds);
            var res = this.getServerResolution();
            var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
            var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
            var z = this.getServerZoom();
            var path = "/static/tiles/"+a.sample+"/" + z + "/" + x + "/" + y + "." + this.type;
            var url = this.url;
            if (OpenLayers.Util.isArray(url)) {
                url = this.selectUrl(path, url);
            }
            if (a.bounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {
                return url + path;
            } else {
                return emptyTileURL;
            }
        }; 
        layer = new OpenLayers.Layer.TMS(this.sample, "",{
            resolutions: [16,8,4,2,1],
            serverResolutions: [64,32,16,8,4,2,1],
            transitionEffect: 'resize',
            alpha: true,
            type: 'png',
            getURL: getURL
        });
        this.map.addLayers([layer]);
    },
    addPoints: function(data){
        var a = this;
        var overlay = new OpenLayers.Layer.Vector("measurements");

        // Add the container when the overlay is added to the map.
        overlay.afterAdd = function () {
            var project = function(x) {
                var point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]));
                return [point.x, point.y];
            }
            var div = d3.selectAll("#" + overlay.div.id);
            div.selectAll("svg").remove();
            var svg = div.append("svg")
                //.attr("width", $("#map").width())
                //.attr("height", $("#map").height());

            var g = svg.append("svg:g");

            var getBounds = function(data){
                xvalues = [];
                yvalues = [];
                $.each(data.features, function(i,el){
                    c = el.geometry.coordinates;
                    xvalues.push(c[0]);
                    yvalues.push(c[1]);
                });
                return [[Math.min.apply(null,xvalues),Math.min.apply(null,yvalues)],
                        [Math.max.apply(null,xvalues),Math.max.apply(null,yvalues)]];
            };

            var bounds = getBounds(data)
            var path = d3.geo.path().projection(project);
            var ramp=d3.scale.sqrt().domain([0,10]).range(["#71eeb8","salmon"]);

            var feature = g.selectAll(".dot")
                .data(data.features)
                .enter().append("path")
                    .attr("class", "dot")
                    .attr("d",path.pointRadius(3))
                    .style("fill", function(d){
                        return ramp(100-d.properties.oxides.Total);
                    })
                    .on("mouseover", a.onMouseMove)

            var reset = function() {
                var bottomLeft = project(bounds[0]),
                topRight = project(bounds[1]);

                svg.attr("width", topRight[0]-bottomLeft[0])
                    .attr("height", bottomLeft[1] - topRight[1])
                    .style("margin-left", bottomLeft[0] + "px")
                    .style("margin-top", topRight[1] + "px");

                g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");

                feature.attr("d", path);
            }
            reset();
            a.map.events.register("moveend", a.map, reset);
        }

        this.map.addLayer(overlay);
    },
    setupEventHandlers: function(){
        var a = this;
        this.events = d3.dispatch("updated");
        this.onMouseMove = function(d,i) {
            d3.select(".dot.selected")
                .attr("class","dot")
            d3.select(this)
                .attr("class","dot selected")
            a.events.updated(d);
        }
    }
});

$(document).ready(function(){
    map = Map("map", map_options);
    map.addPoints(data);

    map.events.on("updated",function(d){
        console.log(d);
        if (typeof dataView === "undefined") dataView = DataView("#data", d);
        else window.dataView.update(d);
    });
});