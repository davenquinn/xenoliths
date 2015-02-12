gulp = require("gulp")
config = require("../config")

gulp.task "watch", ["setWatch", "browserify", "browserSync"], ->
	gulp.watch "#{config.dev}/**/*.scss", ["compass"]

# Note: The browserify task handles js recompiling with watchify
