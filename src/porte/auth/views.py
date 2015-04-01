import requests

from flask import session, request, Blueprint
from flask import render_template, jsonify, redirect, url_for
from werkzeug.security import gen_salt

from porte import db
from porte.oauth.models import Client
from porte.auth.models import Provider
from porte.auth.forms import RegistrationForm, LoginForm
from porte.auth.providers import FacebookProvider
from porte.user.models import User
from porte.auth.helpers import current_user


auth_module = Blueprint('auth', __name__, url_prefix='/auth')

def consumerize(provider, consumer_data, user_data):
    commit = False
    consumer = provider.get_consumer(**consumer_data)
    if not consumer.exists():
        db.session.add(consumer)
        commit = True
    if not consumer.user:
        user = User.query.filter_by(email=user_data['email']).first()
        if user is None:
            user = User(**user_data)
        consumer.user = user
        db.session.add(user)
        commit = True
    if commit:
        db.session.commit()
    return user

@auth_module.route('/', methods=['GET'])
def home():
    user = current_user()
    urls = {
        'email': url_for('auth.email_register'),
        'facebook': url_for('auth.facebook'),
        'logout': url_for('auth.logout')
    }
    return render_template('auth/index.html',
                           user=user,
                           urls=urls)

@auth_module.route('/success', methods=['GET'])
def success():
    user = current_user()
    if user:
        return jsonify(user.json())
    return redirect(url_for('auth.home'))

@auth_module.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(request.referrer or url_for('auth.home'))

# TODO move to email module
@auth_module.route('/email/register', methods=['GET', 'POST'])
def email_register():
    form = RegistrationForm()
    if form.validate():
        provider = Provider.query.filter_by(name='email').first()
        email = form.data['email']
        consumer_data = {
            'email': email,
            'password': form.data['password'],
        }
        user = consumerize(provider, consumer_data, {'email': email})
        session['id'] = user.id
        return redirect(url_for('auth.success'))
    return render_template('auth/email_register.html',
                           errors=form.errors,
                           form=form,
                           action=url_for('auth.email_register'))

# auth module: with type=email|facebook|twitter
@auth_module.route('/email', methods=['GET', 'POST'])
def email_login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate():
            provider = Provider.query.filter_by(name='email').first()
            consumer_data = {
                'email': form.data.email,
                'password': form.data.password
            }
            # TODO get_consumer and exists happens in the consumerize
            consumer = provider.get_consumer(**consumer_data)
            if consumer.exists():
                user = consumerize(provider, consumer_data, {'email': form.data.email})
                session['id'] = user.id
        return redirect(request.form.get('next', url_for('auth.success')))
    user = current_user()
    return render_template('auth/email.html',
                           user=user,
                           action=url_for('auth.email_login'),
                           next=request.args.get('next'))


# TODO move to a facebook module
@auth_module.route('/facebook', methods=['GET', 'POST'])
def facebook():
    provider = FacebookProvider.query.filter_by(name='facebook').first()
    url = url_for('auth.facebook_callback', _external=True)
    return provider.response(url)

@auth_module.route('/facebook/callback')
def facebook_callback():
    provider = FacebookProvider.query.filter_by(name='facebook').first()
    remote = provider.remote
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    # TODO ERROR
    me = requests.get('https://graph.facebook.com/me', params={'access_token': resp['access_token']}).json()
    consumer_data = {
        'id': me['id'],
        'params': resp
    }
    user = consumerize(provider, consumer_data, {'email': me['email']})
    session['id'] = user.id
    return redirect(request.form.get('next', url_for('auth.success')))

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
