
var socket;
function main () {
    socket = io.connect('http://' + location.hostname + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    var text_input = document.getElementById('text');
    var chat = document.getElementById('chat');

    socket.on('status', function(data) {
        chat.value = chat.value + '<' + data.msg + '>\n';
        chat.scrollTop = chat.scrollHeight;
    });
    socket.on('message', function(data) {
        chat.value = chat.value + '<' + data.msg + '>\n';
        chat.scrollTop = chat.scrollHeight;
    });
    text_input.addEventListener('keydown', function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = text_input.value;
            text_input.value = '';
            socket.emit('text', {msg: text});
        }
    });
};
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}
document.addEventListener("DOMContentLoaded", main);