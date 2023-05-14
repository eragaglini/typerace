from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from ..forms import CreateRoomForm, JoinRoomForm

from ..events.room import Room
from ..events.events import socketio, rooms


index_views = Blueprint("index", __name__, template_folder="templates")

def search_room_by_id(id):
    for k, v in rooms.items():
        if v.id == id:
            return v.name
    return ""


@index_views.route("/")
def index():
    return render_template("index.html")


@index_views.route("/create-room", methods=["GET", "POST"])
def create_room():
    """Login form to enter a room."""
    form = CreateRoomForm()
    errors = []
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["room"] = form.room.data
        room = Room(session["room"])

        if room.name not in rooms:
            # appending the newly created room to the rooms global variable
            rooms[room.name] = room
            return redirect(url_for(".chat"))
        else:
            errors.append("Room {0} already exist!".format(session["room"]))
    elif request.method == "GET":
        form.name.data = session.get("name", "")
        form.room.data = session.get("room", "")

    form.name.data = ""
    form.room.data = ""

    return render_template("join_room.html", mode="create", form=form, errors=errors)

@index_views.route("/join", methods=["GET", "POST"])
@index_views.route('/join/<room_code>', methods=["GET", "POST"])
def join_room(room_code = False):
    """Login form to enter a room."""
    form = JoinRoomForm()
    errors = []
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["room"] = form.room.data if form.room.data in rooms else search_room_by_id(form.room.data)
        if session["room"]:
            return redirect(url_for(".chat"))
        else:
            errors.append("Room {0} doesn't exist!".format(session["room"]))
    elif request.method == "GET":
        form.name.data = session.get("name", "")
        form.room.data = session.get("room", "")

    form.name.data = ""
    form.room.data = room_code if room_code else ""

    return render_template("join_room.html", mode="join", form=form, errors=errors)


@index_views.route("/chat")
def chat():
    name = session.get("name", "")
    room = session.get("room", "")
    if name == "" or room == "" or room not in rooms:
        return redirect(url_for(".index"))
    return render_template("base_game.html", name=name, room=room)


@index_views.route("/server-browser")
def browse_rooms():
    return render_template("browse_rooms.html", rooms=rooms)
