from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators


class RegistrationForm(Form):
    email = TextField('Email Address', [
        validators.Required(),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password')


class LoginForm(Form):
    email = TextField('Email Address', [
        validators.Required(),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.Required(),
    ])
