from flask import Blueprint, session, redirect, url_for, render_template, request
from ..forms import LoginForm

index_views = Blueprint('index', __name__, template_folder='templates')


@index_views.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.checkers'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)

@index_views.route('/checkers')
def checkers():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('checkers.html', name=name, room=room)