import unittest
import os

from porte import app, db
from porte.auth.providers import FacebookProvider
from porte.auth.models import Provider


class ProviderTestCase(unittest.TestCase):
    def setUp(self):
        app.config['test'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASE_DIR'], 'test.db')
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        db.create_all()
        if hasattr(self, 'data'):
            self.data()

    def add_provider(self):
        provider = Provider(name=self.form['type'])
        db.session.add(provider)
        db.session.commit()
        return provider

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class EmailProviderTestCase(ProviderTestCase):
    def data(self):
        self.form = {
            'type': 'email',
            'data': {
                'username': 'boertel',
                'password': 'password',
            }
        }
        self.data = self.form['data']

    def test_user_doesnt_exist(self):
        provider = self.add_provider()
        consumer = provider.get_consumer(**self.data)
        assert consumer.username == self.data['username']
        assert consumer.password != self.data['password']
        assert consumer.exists() == False

    def test_user_exists(self):
        provider= self.add_provider()
        consumer = provider.get_consumer(**self.data)
        assert consumer.exists() == False
        db.session.add(consumer)
        db.session.commit()
        assert consumer.exists() == True
        assert consumer.provider == provider


'''
class FacebookProviderTestCase(ProviderTestCase):
    def test_user_doesnt_exist(self):
        params = {
            'app_id': '1234567890',
            'app_secret': 'abcdefghijkl',
        }
        provider = FacebookProvider()
        provider.params = params
        db.session.add(provider)
        db.session.commit()
        assert provider.params['app_id'] == params['app_id']
        callback_url = url_for('auth.facebook_callback')
        print provider.response(callback_url)
'''


if __name__ == '__main__':
    unittest.main()
