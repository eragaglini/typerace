var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('join', {'username': "test"});
    });
    socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            var text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
        }
    });
    
    $('#leave').click(() => leave_room());

});

function leave_room() {
    socket.emit('leave', {}, function() {
        socket.disconnect();
        // go back to the main page
        window.location.href = "/";
    });
}
