var map;
var mapBounds = new OpenLayers.Bounds( 0.0, -8640.0, 8577.0, 0.0);
var mapMinZoom = 0;
var mapMaxZoom = 7;
var emptyTileURL = "http://www.maptiler.org/img/none.png";
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;

var layer;
var vlayer;
var dataPane;
var GeoJSON = new OpenLayers.Format.GeoJSON();

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

var addPoints = function(data){
    string = JSON.stringify(data);
    vlayer.addFeatures(GeoJSON.read(string));
    selectFeatures = new SelectFeaturesControl(vlayer);
    map.addControl(selectFeatures);
}; 

var init = function(){
    var options = {
        div: "map",
        controls: [],
        maxExtent: new OpenLayers.Bounds(0.0, -8640.0, 8577.0, 0.0),
        maxResolution: 64.000000,
        numZoomLevels: 8
    };
    map = new OpenLayers.Map(options);
    //dataPane = new DataPane();

    layer = new OpenLayers.Layer.TMS("CK-2", "",{
        resolutions: [16,8,4,2,1],
        serverResolutions: [64,32,16,8,4,2,1],
        transitionEffect: 'resize',
        alpha: true,
        type: 'png',
        getURL: getURL
    });

    map.addLayer(layer);

    vlayer = new OpenLayers.Layer.Vector("Measurements");
    map.addLayer(vlayer);

    map.zoomToExtent(mapBounds);

    map.addControls([new OpenLayers.Control.Zoom(),
                     new OpenLayers.Control.Navigation(),
                     new OpenLayers.Control.MousePosition({numDigits:2}),
                     new OpenLayers.Control.ArgParser(),
                     new OpenLayers.Control.Attribution()]);

    //$.get('/data/CK-2.json', addPoints);
    addPoints(data);

};

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
    if (mapBounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {
        return url + path;
    } else {
        return emptyTileURL;
    }
};

/*d3.json('/data/CK-2.json', function (collection) {
    var overlay = new OpenLayers.Layer.Vector("measurements");

    // Add the container when the overlay is added to the map.
    overlay.afterAdd = function () {

        var div = d3.selectAll("#" + overlay.div.id);
        div.selectAll("svg").remove();
        var svg = div.append("svg");
        g = svg.append("g");

        var bounds = d3.geo.bounds(collection),
            path = d3.geo.path().projection(project);

        var feature = g.selectAll("path")
            .data(collection.features)
            .enter().append("path")
            .attr("d", path.pointRadius(5))
            .on("mouseover", function (d) {
            var mousePosition = d3.svg.mouse(this);
            $("#pop-up").fadeOut(100, function () {
                // Popup content
                $("#pop-up-title").html("HELLO");
                //$("#pop-img").html(d.properties.mag);
                //$("#pop-desc").html(d.properties.place);

                // Popup position
                var popLeft = mousePosition[0] + 300 > screen.width ?
                    mousePosition[0] - 400 : mousePosition[0];
                var popTop = mousePosition[1];
                $("#pop-up").css({
                    "left": popLeft + 50,
                    "top": popTop
                });
                $("#pop-up").fadeIn(100);
            });
        }).
        on("mouseout", function () {
            $("#pop-up").fadeOut(50);
        });

        map.events.register("moveend", map, reset);

        reset();


        function reset() {

            var bottomLeft = project(bounds[0]),
                topRight = project(bounds[1]);

            svg.attr("width", bottomLeft[0]-topRight[0])
                .attr("height", bottomLeft[1] - topRight[1])
                .style("margin-left", bottomLeft[0] + "px")
                .style("margin-top", topRight[1] + "px");

            g.attr("transform", "translate(" + -bottomLeft[0] + "," + -topRight[1] + ")");

            feature.attr("d", path);
        }

        function project(x) {
            var point = map.getViewPortPxFromLonLat(new OpenLayers.LonLat(x[0], x[1]));
            return [point.x, point.y];
        }
    }

    map.addLayer(overlay);



});*/



$(document).ready(function(){
    init();
});