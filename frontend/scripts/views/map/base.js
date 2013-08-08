define([
    "views/base/generic",
    "openlayers", 
    "options",
    "views/base/colors"
    ],function(GenericView, OpenLayers, Options, Colorizer){

    Map = GenericView.extend({
        initialize: function(){
            this.render()
            this.colors = Colorizer;
        },
        render: function(){
            this.changeSample(this.options.sample);
            return this
        },
        startMap: function(){
            this.bounds = OpenLayers.Bounds.fromArray(this.sample.bounds);
             var Options = {
                div: this.el,
                controls: [],
                maxExtent: this.bounds,
                //restrictedExtent: this.bounds,
                maxResolution: 64.000000,
                numZoomLevels: 8
            };
            this.map = new OpenLayers.Map(Options);
            this.GeoJSON = new OpenLayers.Format.GeoJSON();

            this.map.addControls([new OpenLayers.Control.Zoom(),
                     new OpenLayers.Control.Navigation(),
                     //new OpenLayers.Control.KeyboardDefaults(),
                     new OpenLayers.Control.MousePosition({numDigits:2}),
                     new OpenLayers.Control.ArgParser()]);

            this.setupTiles();
            this.map.zoomToExtent(this.bounds);
           
        },
        setupTiles: function(){
            var a = this;
            var getURL = function(bounds) {
                var mapMinZoom = 0;
                var mapMaxZoom = 8;
                var emptyTileURL = "http://www.maptiler.org/img/none.png";
                bounds = this.adjustBounds(bounds);
                var res = this.getServerResolution();
                var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
                var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
                var z = this.getServerZoom();
                var path = "/static/tiles/"+a.options.sample+"/" + z + "/" + x + "/" + y + "." + this.type;
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
        changeSample: function(sample){
            this.sample = Options["samples"][sample]
            this.startMap();
        }
    });
    return Map;
});
