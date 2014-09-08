app = "modules/xenoliths/application"

module.exports =
    app: app
    dev: "#{app}/frontend"
    dist: "#{app}/static"
    endpoints:
        main: "./#{app}/frontend/scripts/main"
