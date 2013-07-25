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
    __init__: function(div){
        this.bounds = new OpenLayers.Bounds( 0.0, -8640.0, 8577.0, 0.0);

        var options = {
            div: div,
            controls: [],
            maxExtent: this.bounds,
            maxResolution: 64.000000,
            numZoomLevels: 8
        };
        this.map = new OpenLayers.Map(options);
        this.GeoJSON = new OpenLayers.Format.GeoJSON();

        this.map.addControls([new OpenLayers.Control.Zoom(),
                 new OpenLayers.Control.Navigation(),
                 new OpenLayers.Control.MousePosition({numDigits:2}),
                 new OpenLayers.Control.ArgParser()]);

        this.setupTiles()
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
            var path = "/static/tiles/CK-2/" + z + "/" + x + "/" + y + "." + this.type;
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
        layer = new OpenLayers.Layer.TMS("CK-2", "",{
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
            var div = d3.selectAll("#" + overlay.div.id);
            div.selectAll("svg").remove();
            var svg = div.append("svg");
            var g = svg.append("g");

            var bounds = d3.geo.bounds(data),
                path = d3.geo.path().projection(project);

            var project = function(x) {
                var point = a.map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]));
                return [point.x, point.y];
            }

            var feature = g.selectAll(".dot")
                .data(data.features)
                .enter().append("circle")
                    .attr("class", "dot")
                    .attr("r",3.5)

            var reset = function() {

                var bottomLeft = project(bounds[0]),
                    topRight = project(bounds[1]);

                svg.attr("width", bottomLeft[0]-topRight[0])
                    .attr("height", bottomLeft[1] - topRight[1])
                    .style("margin-left", bottomLeft[0] + "px")
                    .style("margin-top", topRight[1] + "px");

                g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");

                feature
                    .attr("cx",function(d){return project(d.geometry.coordinates)[0]})
                    .attr("cy",function(d){return project(d.geometry.coordinates)[1]})
                    .style("fill","lightblue")
            }

            a.map.events.register("moveend", a.map, reset);
            reset();

        }

        this.map.addLayer(overlay);
    }
    /*addPoints: function(data){
        vlayer = new OpenLayers.Layer.Vector("Measurements", {
            style: {}
        });
        this.map.addLayer(vlayer);

        string = JSON.stringify(data);
        vlayer.addFeatures(this.GeoJSON.read(string));
        this.selectFeatures = new SelectFeaturesControl(vlayer);
        this.map.addControl(this.selectFeatures);
    },
    joinData: function(data){
        d3.selectAll("#map circle")
            .data(data, function(d) { return (d && d.key) || d3.select(this).attr("id"); })
            .text(function(d) { return d.val; });
    }*/
});

$(document).ready(function(){
    map = Map("map");
    map.addPoints(data);
});