from .. import PorteTestCase

from porte import db

from porte.auth.providers import EmailProvider


class ViewsTestCase(PorteTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.provider = EmailProvider()
        db.session.add(self.provider)
        db.session.commit()

    def test_email_register(self):
        form = {
            'email': 'ben@oertel.fr',
            'password': 'password',
            'confirm': 'password',
        }

        response = self.post('/auth/email/register', data=form)
        self.assertTrue(False)
