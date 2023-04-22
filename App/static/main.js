
var socket;
function main () {
    console.log("caricato main.js")
    socket = io.connect('http://' + location.hostname + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    var text_input = document.getElementById('text');
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