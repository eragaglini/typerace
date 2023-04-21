from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_session import Session

from App.config import config

from App.views import views

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def configure_app(app, config, overrides):
    for key, value in config.items():
        if key in overrides:
            app.config[key] = overrides[key]
        else:
            app.config[key] = config[key]

socketio = SocketIO()

def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path='/static')
    socketio.init_app(app)
    configure_app(app, config, config_overrides)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEVER_NAME'] = '0.0.0.0'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    # This means that the session cookies won’t expire when the browser closes
    app.config["SESSION_PERMANENT"] = True
    # This means that the cookies are going to be stored locally on the server-side
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    CORS(app)
    add_views(app)
    app.app_context().push()
    return app