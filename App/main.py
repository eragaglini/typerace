from flask import Flask
from flask_cors import CORS

from App.config import config
from App.views import views
from App.events import socketio


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def configure_app(app, config, overrides):
    for key, value in config.items():
        if key in overrides:
            app.config[key] = overrides[key]
        else:
            app.config[key] = config[key]


def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path="/static")
    socketio.init_app(app)
    configure_app(app, config, config_overrides)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEVER_NAME"] = "0.0.0.0"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    CORS(app)
    add_views(app)
    app.app_context().push()
    return app
