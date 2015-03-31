import unittest
import os

from porte import app, db


class AuthTestCase(unittest.TestCase):
    def setup(self):
        app.config['test'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config.BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_email_provider(self):
        pass

if __name__ == '__main__':
    unittest.main()
