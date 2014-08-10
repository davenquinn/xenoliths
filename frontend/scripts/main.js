var $ = require('jquery');
var Backbone = require('backbone');
var startApp = require('./app');

    console.log("Starting to get data");
    $("body").append("<img class='loading' src='/static/images/ajax-loader.gif' />");
    $.ajax({
        url: "/data/data.json?bust=" +  (new Date()).getTime(),
        dataType:"json",
        success: startApp,
        error: function(request, textStatus, errorThrown) {
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
