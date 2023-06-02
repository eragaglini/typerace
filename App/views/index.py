from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from ..forms import CreateRoomForm, JoinRoomForm

from ..events.room import Room
from ..events.events import (
    get_room_by_id,
    get_room_by_name,
    add_room,
    remove_room,
    rooms,
)
import uuid


index_views = Blueprint("index", __name__, template_folder="templates")


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
        room = {"id": str(uuid.uuid4())[:5], "name": form.room.data, "users_num": 0}

        if not get_room_by_name(room["name"]):
            # appending the newly created room to the rooms global variable
            add_room(room=room)
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
@index_views.route("/join/<room_code>", methods=["GET", "POST"])
def join_room(room_code=False):
    """Login form to enter a room."""
    form = JoinRoomForm()
    errors = []
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["room"] = (
            form.room.data
            if get_room_by_name(form.room.data)
            else get_room_by_id(form.room.data)
        )
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
    if name == "" or room == "" or not get_room_by_name(room):
        return redirect(url_for(".index"))
    return render_template("base_game.html", name=name, room=room)


@index_views.route("/server-browser")
def browse_rooms():
    return render_template("browse_rooms.html", rooms=rooms)
