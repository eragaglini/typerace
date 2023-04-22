from flask import Blueprint, render_template, request
from flask import session
from flask import request
import random

index_views = Blueprint("index_views", __name__, template_folder="../templates")

@index_views.route("/", methods=["GET", "POST"])
def index_page():
    return render_template("index.html")
