from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.oauthlib.provider import OAuth2Provider
from flask.ext.oauthlib.client import OAuth


app = Flask(__name__, template_folder='templates')
app.config.from_object('config')

db = SQLAlchemy(app)
oauth_provider = OAuth2Provider(app)
oauth_client = OAuth(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from porte.auth.views import auth_module
from porte.user.api import api_module
from porte.oauth.views import *
from porte.oauth.helpers import *

app.register_blueprint(auth_module)
app.register_blueprint(api_module)
