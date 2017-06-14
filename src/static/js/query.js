$(document).ready(function(){
    (function ($) {
            $.getUrlParam = function (name) {
                var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
                var r = window.location.search.substr(1).match(reg);
                if (r != null) return unescape(r[2]); return null;
            }
        })(jQuery);
    var name_id = $.getUrlParam('name_id');
    console.log('ws://' + document.domain + ':' + location.port+'/')
    var socket = io.connect('http://' + document.domain + ':' + location.port+'/'+name_id);
    socket.on('last_log', function(log) {
            console.log(log)
            $('#real_log').html($('#real_log').html()+'</br>'+log)
        });
});
