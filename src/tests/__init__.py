import os
import json
from unittest import TestCase

from porte import app, db


class PorteTestCase(TestCase):
    def _create_app(self):
        app.config['test'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'\
            + os.path.join(app.config['BASE_DIR'], 'tests/test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def _request(self, method, *args, **kwargs):
        kwargs['follow_redirects'] = kwargs.get('follow_redirects', True)
        response = method(*args, **kwargs)
        if response.content_type == 'application/json':
            response.json = json.loads(response.data)
        return response

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request(self.client.post, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request(self.client.put, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request(self.client.delete, *args, **kwargs)

    def setUp(self):
        super(PorteTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        super(PorteTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()
