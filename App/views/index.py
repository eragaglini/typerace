from flask import Blueprint, render_template, request
from flask import session
from flask import request
import random

index_views = Blueprint("index_views", __name__, template_folder="../templates")


def generate_dungeon(w, h):
    session["dungeon"] = []
    wumpus_x = random.randrange(2, w)
    wumpus_y = random.randrange(2, h)
    gold_x = random.randrange(2, w)
    gold_y = random.randrange(2, h)
    while gold_x == wumpus_x and gold_y == wumpus_y:
        gold_x = random.randrange(2, w)
        gold_y = random.randrange(2, h)
    for i in range(h):
        line = []
        # 0 - free
        # 1 - pit
        # 2 - wumpus
        for j in range(w):
            if (i == 0 or i == 1) and (j == 0 or j == 1):
                # the beginning of the dungeon cannot have pits or wumpus
                line.append(0)
            elif i == wumpus_x and j == wumpus_y:
                # wumpus location
                line.append(2)
            elif i == gold_x and j == gold_y:
                # gold location
                line.append(3)
            elif ((i == wumpus_x - 1 or i == wumpus_x + 1) and (j == wumpus_y)) or (
                (j == wumpus_y - 1 or j == wumpus_y + 1) and (i == wumpus_x)
            ):
                # nothing around the wumpus
                line.append(0)
            else:
                # random pits distributed
                if random.random() <= 0.15:
                    line.append(1)
                else:
                    line.append(0)

        session["dungeon"].append(line)
    session["curr_pos"] = [0, 0]
    return render_template("game.html", width=w, height=h)


@index_views.route("/", methods=["GET", "POST"])
def index_page():
    if request.method == "POST":
        session["width"] = int(request.form["width"])
        session["height"] = int(request.form["height"])
        return generate_dungeon(session["width"], session["height"])
    return render_template("index.html")
