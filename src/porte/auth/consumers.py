from werkzeug.security import generate_password_hash

from porte.auth.models import Consumer


class EmailConsumer(Consumer):
    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email')
        self.password = generate_password_hash(kwargs.pop('password'))
        kwargs['uid'] = self.email
        super(EmailConsumer, self).__init__(*args, **kwargs)

    def get_verify_token(self):
        key = '%s:%s' % (self.email, self.password)
        return generate_password_hash(key)


class FacebookConsumer(Consumer):
    def __init__(self, *args, **kwargs):
        kwargs['uid'] = kwargs.pop('id')
        super(FacebookConsumer, self).__init__(*args, **kwargs)

    def get_verify_token(self):
        return self.uid
