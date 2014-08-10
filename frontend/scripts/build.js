var fs = require('fs');
var path = require('path');
var browserify = require('browserify');
var shim = require('browserify-shim');

var bundled = browserify({ debug: true })
    .use(shim({ alias: 'openlayers', path: 'lib/openlayers/OpenLayers', exports: 'OpenLayers' }))
    .use(shim({ alias: 'jquery.bootstrap', path: 'lib/bootstrap/dist/js/bootstrap', exports: null }))
    .use(shim({ alias: 'jquery.slider', path: 'lib/jquery-simple-slider/js/simple-slider', exports: null }))
    .use(shim({ alias: 'jquery.switch', path: 'lib/bootstrap-switch/static/js/bootstrap-switch', exports: null }))
    .addEntry(path.join(__dirname, 'main.js'))
    .bundle();

fs.writeFileSync(path.join(__dirname, 'build/bundle.js'), bundled, 'utf-8');
