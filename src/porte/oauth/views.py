from urllib import quote

from flask import url_for, request, redirect, render_template, jsonify

from werkzeug.security import gen_salt

from porte import app, oauth_provider, db
from porte.auth.helpers import current_user
from porte.oauth.models import Client


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth_provider.authorize_handler
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

@app.route('/oauth/token', methods=['POST'])
@oauth_provider.token_handler
def access_token():
    return None

@app.route('/oauth/revoke', methods=['POST'])
@oauth_provider.revoke_handler
def revoke_token():
    pass

# TODO more management ? than oauth
@app.route('/client')
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
