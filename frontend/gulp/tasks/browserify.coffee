browserify = require("browserify")
watchify = require("watchify")
bundleLogger = require("../util/bundleLogger")
gulp = require("gulp")
handleErrors = require("../util/handleErrors")
source = require("vinyl-source-stream")
coffeeify = require("coffeeify")
hbsfy = require("hbsfy").configure
	extensions: ["html"]
config = require('../config')

setupEndpoint = (name,location) ->
	#bundleMethod = (if global.isWatching then watchify else browserify)
	debug = (if global.dist then false else true)

	bundler = browserify
		entries: [location]
		extensions: [".coffee"]
		debug: debug
		cache: {}
		packageCache: {}
		fullPaths: true

	if global.isWatching
		bundler = watchify(bundler)

	bundler
		.transform coffeeify
		.transform hbsfy

	if global.dist
		bundler.transform {global: true}, 'uglifyify'

	bundle = ->
		bundleLogger.start()
		bundler
			.bundle()
			.on("error", handleErrors)
			.on "end", bundleLogger.end
			.pipe(source("#{name}.min.js"))
			.pipe(gulp.dest("#{config.dist}/scripts/"))

	# Rebundle with watchify on changes
	if global.isWatching
		bundler.on "update", bundle
	bundle()

gulp.task "browserify", ->
	for name, location of config.endpoints
		setupEndpoint(name, location)
