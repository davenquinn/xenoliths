browserSync = require("browser-sync")
config = require("../config")
gulp = require("gulp")
gulp.task "browserSync", ->
	browserSync.init [
		"#{config.dist}/scripts/*.js"
		"#{config.dist}/styles/*.css"
	], proxy: "0.0.0.0:8000"
