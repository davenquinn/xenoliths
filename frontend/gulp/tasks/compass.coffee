gulp = require("gulp")
plumber = require("gulp-plumber")
compass = require("gulp-compass")
autoprefixer = require("gulp-autoprefixer")
notify = require("gulp-notify")
handleErrors = require("../util/handleErrors")
config = require("../config")
cssmin = require("gulp-cssmin")
path = require("path")

gulp.task "compass", ->
    console.log config.dist
    debug = (if global.dist then false else true)
    pipeline = gulp.src("#{config.dev}/styles/screen.scss")
        .pipe plumber()
        .pipe compass
            css: "css"
            sass: "#{path.resolve(config.dev)}/styles"
            image: "images"
            sourcemap: debug
            debug: debug
            #import_path: "#{config.dev}/styles"
        .pipe autoprefixer("last 1 version")
        .on "error", handleErrors

    if not debug
        pipeline = pipeline.pipe(cssmin())

    pipeline
        .pipe gulp.dest("#{config.dist}/styles")
