app = "xenoliths"

module.exports =
    app: app
    dev: "#{app}/_frontend"
    dist: "#{app}/application/static"
    endpoints:
        main: "./#{app}/_frontend/main"
