var $ = require('jquery');
var GenericView = require('../base/generic');
var template = require('../../text!templates/controls/raw-data.html');


RawViewer = GenericView.extend({
    initialize: function(){
        var a = this;
        this.parent = this.options.parent;
        this.map = this.options.map;
        this.compile(template);
        this.map.dispatcher.on("updated.raw",function(d){
            a.update(d)
        });
        if (this.map.selected) {
            this.update(this.map.selected)
        } else this.update(this.map.data.features[0])
    },
    events: {
        "click button.close": "destroy"
    },
    syntaxHighlight: function(json) {
        if (typeof json != 'string') {
             json = JSON.stringify(json, undefined, 2);
        }
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            var cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    },
    update: function(data){
        if (typeof(data) === "undefined") return;
        this.$el.html("<pre>"+this.syntaxHighlight(data)+"</pre>");
    }
});
module.exports = RawViewer;

