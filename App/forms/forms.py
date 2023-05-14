from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateRoomForm(FlaskForm):
    """Accepts a nickname and a room."""

    name = StringField("Name", validators=[DataRequired()])
    room = StringField("Room Name", validators=[DataRequired()])
    submit = SubmitField("Enter Chatroom")


class JoinRoomForm(FlaskForm):
    """Accepts a nickname and a room."""

    name = StringField("Name", validators=[DataRequired()])
    room = StringField("Room Name", validators=[DataRequired()])
    submit = SubmitField("Enter Chatroom")
