from flask.ext.wtf import Form
from wtforms import TextField, validators


class UserForm(Form):
    first_name = TextField('First name')
    last_name = TextField('Last name')
    email = TextField('Email Address', [
        validators.Required(),
        validators.Email(),
    ])
