gulp = require("gulp")
config = require("../config")

gulp.task "watch", ["setWatch", "browserify", "browserSync"], ->
	gulp.watch "#{config.dev}/styles/screen.scss", ["compass"]

# Note: The browserify task handles js recompiling with watchify
