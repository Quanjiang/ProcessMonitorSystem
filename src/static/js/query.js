$(document).ready(function(){
    (function ($) {
            $.getUrlParam = function (name) {
                var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
                var r = window.location.search.substr(1).match(reg);
                if (r != null) return unescape(r[2]); return null;
            }
        })(jQuery);
    var name_id = $.getUrlParam('name_id');

    alert('ws://' + document.domain + ':' + location.port+'/')
    var socket = io.connect('ws://' + document.domain + ':' + location.port+'/');
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });
});
