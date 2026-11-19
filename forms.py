"""Formularios de la aplicación."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(max=128)])
