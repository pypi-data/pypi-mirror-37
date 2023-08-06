
$(function() {

    namespace = '/main';


    var $window = $(window);


    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
}