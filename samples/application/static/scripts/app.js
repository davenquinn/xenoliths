define([
    "jquery",
    "backbone",
    "router",
    "data"
    ],function($, Backbone, Router, Data){
    var App = {
        JSON_RPC: function(method, params, callback){
            var url = "/json/";
            request = {
                method: method,
                params: params,
                jsonrpc: "2.0",
                id: 1
            };
            req = JSON.stringify(request);
            console.log(req);
            $.post(url, req, callback, "json");
        }
    };
    var startApp = function(data){
        window.App = App;
        App["Data"] = new Data(data);
        App["Router"] = new Router();
        Backbone.history.start();
    };
    return startApp;
});
