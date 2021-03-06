gulp = require 'gulp'
util = require 'gulp-util'

gulp.task "build", [
    "compass"
]

gulp.task 'setDist', ->
    util.log "Bunding for distribution."
    global.dist = true

gulp.task "dist", ["setDist", "build"]

gulp.task 'default', [
        'build'
        'backend'
        'watch'
    ]

# A task to allow you to serve compressed files.
gulp.task 'stage', [
        'setDist'
        'default'
    ]
