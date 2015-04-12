from werkzeug.security import generate_password_hash, check_password_hash

from porte.auth.models import Consumer


class EmailConsumer(Consumer):
    def __init__(self, *args, **kwargs):
        if kwargs.get('params') and kwargs['params']['password']:
            kwargs['params'] = {
                'password': generate_password_hash(kwargs['params']['password'])
            }
        super(EmailConsumer, self).__init__(*args, **kwargs)

    def is_valid(self, params):
        return check_password_hash(self.params['password'], params['password'])


# TODO need to be remove
class FacebookConsumer(Consumer):
    pass
