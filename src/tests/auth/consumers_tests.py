from .. import PorteTestCase

from porte import db
from porte.auth.models import Consumer
from porte.auth.providers import EmailProvider
from porte.auth.consumers import EmailConsumer


class EmailProviderTestCase(PorteTestCase):
    def setUp(self):
        super(EmailProviderTestCase, self).setUp()
        self.provider = EmailProvider()
        db.session.add(self.provider)
        db.session.commit()

    def test_create_consumer(self):
        email = 'boertel'
        params = {'password': 'password'}
        consumer, created = Consumer.get_or_create(provider=self.provider,
                                                   uid=email,
                                                   params=params)
        self.assertTrue(isinstance(consumer, EmailConsumer))
        self.assertTrue(created)
        self.assertEqual(consumer.uid, email)
        self.assertIsNotNone(consumer.params['password'])

    def test_get_consumer(self):
        email = 'boertel'
        consumer, created = Consumer.get_or_create(provider=self.provider,
                                                   uid=email)
        self.assertTrue(created)
        consumer, created = Consumer.get_or_create(provider=self.provider,
                                                   uid=email)
        self.assertFalse(created)

    def test_consumer_is_not_valid(self):
        email = 'boertel'
        params = {'password': 'password'}
        consumer, created = Consumer.get_or_create(provider=self.provider,
                                                   uid=email,
                                                   params=params)
        self.assertTrue(created)
        self.assertFalse(consumer.is_valid({'password': 'wrong'}))

    def test_consumer_is_valid(self):
        email = 'boertel'
        params = {'password': 'password'}
        consumer, created = Consumer.get_or_create(provider=self.provider,
                                                   uid=email,
                                                   params=params)
        self.assertTrue(created)
        self.assertTrue(consumer.is_valid({'password': 'password'}))
