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


            this.navControl = new OpenLayers.Control.Navigation()
            this.map.addControls([new OpenLayers.Control.Zoom(),
                     this.navControl,
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
                var mapMaxZoom = 7;
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
                resolutions: [16,8,4,2,1,0.5],
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
            this.sample_name = sample;
            this.startMap();
        },
        zoomToPoint: function(point, level){
            var centerPoint = new OpenLayers.LonLat(point[0],point[1]);      
            this.map.setCenter(centerPoint, level); 
        },
        setDraggable: function(bool){
            if (bool) {
                this.navControl.activate()
            } else {
                this.navControl.deactivate()
            }
        }
    });
    return Map;
});
