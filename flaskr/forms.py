from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import Email
from wtforms.validators import InputRequired
from wtforms.validators import Length


class LoginForm(FlaskForm):
    """LoginForm class to store login information."""

    username = StringField('', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "username"})
    password = PasswordField('', validators=[InputRequired(), Length(
        min=4, max=80)], render_kw={"placeholder": "password"})
    remember = BooleanField('remember')


class RegisterForm(FlaskForm):
    """RegisterForm class to store register form."""

    email = StringField('', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)], render_kw={"placeholder": "email"})
    username = StringField('', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "username"})
    password = PasswordField('', validators=[InputRequired(), Length(
        min=4, max=80)], render_kw={"placeholder": "password"})
