from flask import session, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from first import first

socketio = SocketIO()

rooms = []


def get_room_by_name(name):
    return first(rooms, key=lambda item: item["name"] == name)


def get_room_by_id(id):
    return first(rooms, key=lambda item: item["id"] == id)


def add_room(room):
    rooms.append(room)


def remove_room(room):
    rooms[:] = [d for d in rooms if d.get("id") != room["id"]]


@socketio.on("join", namespace="/chat")
def on_join(data):
    """User joins a room"""
    room = get_room_by_name(session.get("room"))
    if not room:
        emit("redirect", {"url": url_for("index.index")})
        return
    else:
        room["users_num"] += 1

    username = session.get("name")
    room_name = session.get("room")
    join_room(room_name)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room_name + " room."}, room=room_name)


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
    room_name = session.get("room")

    room = get_room_by_name(session.get("room"))
    room["users_num"] -= 1
    if room["users_num"] == 0:
        remove_room(room=room)

    leave_room(room_name)
    send({"msg": username + " has left the room."}, to=room_name)
