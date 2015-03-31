from porte import oauth_client
from porte.auth.models import Provider


class EmailProvider(Provider):
    __mapper_args__ = {
        'polymorphic_identity': 'email',
    }


class FacebookProvider(Provider):
    __mapper_args__ = {
        'polymorphic_identity': 'facebook',
    }

    @property
    def remote(self):
        # TODO or would be better to do it on the __init__ after the filter
        remote = oauth_client.remote_app(
            'facebook',
            register=False,
            base_url='https://graph.facebook.com/',
            request_token_url=None,
            access_token_url='/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            consumer_key=self.params['app_id'],
            consumer_secret=self.params['app_secret'],
            request_token_params={'scope': 'email'}
        )
        return remote

    def response(self, callback_url):
        return self.remote.authorize(callback=callback_url)
