from urllib import quote

from flask import session, request, Blueprint
from flask import render_template, jsonify, redirect, url_for
from werkzeug.security import gen_salt

from porte import oauth, db
from porte.auth.models import Client
from porte.user.models import User
from porte.auth.helpers import current_user


auth_module = Blueprint('auth', __name__, url_prefix='/oauth')


# auth module: with type=email|facebook|twitter
@auth_module.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect(request.form.get('next', url_for('auth.home')))
    user = current_user()
    return render_template('auth/home.html', user=user, next=request.args.get('next'))

@auth_module.route('/client')
def client():
    user = current_user()
    if not user:
        return redirect(url_for('auth.home'))
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
        ]),
        _default_scopes='email',
        user_id=user.id
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(client_id=item.client_id, client_secret=item.client_secret)

# TODO oauth module
@auth_module.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect('%s?next=%s' % (url_for('auth.home'), quote(request.url)))
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('auth/authorize.html', **kwargs)
    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@auth_module.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None

@auth_module.route('/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    pass
