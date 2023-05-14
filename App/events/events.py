from flask import session, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, send

socketio = SocketIO()

rooms = {}


@socketio.on("join", namespace="/chat")
def on_join(data):
    """User joins a room"""
    if session.get("room") not in rooms:
        emit('redirect', {'url': url_for('index.index')})
        return

    username = session.get("name")
    room = session.get("room")
    join_room(room)

    if room in rooms:
        rooms[room].users_num += 1

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    emit("message", {"msg": session.get("name") + ":" + message["msg"]}, room=room)


@socketio.on("leave", namespace="/chat")
def on_leave(data):
    """User leaves a room"""
    username = session.get("name")
    room = session.get("room")

    rooms[room].users_num -= 1
    if rooms[room].users_num == 0:
        del rooms[room]

    leave_room(room)
    send({"msg": username + " has left the room."}, to=room)
