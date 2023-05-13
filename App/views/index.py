from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from ..forms import CreateRoomForm, JoinRoomForm

from ..events import socketio, rooms


index_views = Blueprint('index', __name__, template_folder='templates')


@index_views.route('/')
def index():
    return render_template('index.html')

@index_views.route('/create-room', methods=['GET', 'POST'])
def create_room():
    """Login form to enter a room."""
    form = CreateRoomForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')

    return render_template('create_room.html', form=form)


@index_views.route('/join', methods=['GET', 'POST'])
def join_room():
    """Login form to enter a room."""
    form = JoinRoomForm()
    errors = []
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('create_room.html', form=form, errors=errors)

@index_views.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('base_game.html', name=name, room=room)