from flask import Blueprint, render_template, request
from flask import session
from flask import request

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    if request.method == 'POST':
        session['width'] = int(request.form['width'])
        session['height'] = int(request.form['height'])
        return render_template('game.html')
    return render_template('index.html')