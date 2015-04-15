from .. import PorteTestCase

from porte import db

from porte.auth.providers import EmailProvider


class ViewsTestCase(PorteTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.provider = EmailProvider()
        db.session.add(self.provider)
        db.session.commit()

    def test_email_register_with_valid_email(self):
        form = {
            'email': 'ben@oertel.fr',
            'password': 'password',
            'confirm': 'password',
        }

        response = self.post('/auth/email/register', data=form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'ben@oertel.fr')

    def test_email_register_with_invalid_email(self):
        form = {
            'email': 'benoertel.fr',
            'password': 'password',
            'confirm': 'password',
        }
        response = self.post('/auth/email/register', data=form)
        self.assertEqual(response.status_code, 400)

    def test_email_register_with_invalid_password(self):
        form = {
            'email': 'ben@oertel.fr',
            'password': 'password',
            'confirm': 'notthesame',
        }
        response = self.post('/auth/email/register', data=form)
        self.assertEqual(response.status_code, 400)
