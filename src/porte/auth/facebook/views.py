import requests
from flask import request, url_for, session, redirect
from porte.auth.providers import FacebookProvider
from porte.auth.helpers import consumerize


def index():
    provider = FacebookProvider.query.filter_by(name='facebook').first()
    url = url_for('auth.facebook_callback', next=request.args.get('next'),
                  _external=True)
    return provider.response(url)


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
    me = requests.get('https://graph.facebook.com/me',
                      params={'access_token': resp['access_token']}).json()
    consumer_data = {
        'id': me['id'],
        'params': resp
    }
    user = consumerize(provider, consumer_data, {'email': me['email']})
    session['id'] = user.id
    return redirect(request.args.get('next', url_for('auth.success')))
