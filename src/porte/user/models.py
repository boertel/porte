from datetime import datetime

from porte import db
from sqlalchemy import event
from sqlalchemy_utils import ChoiceType


class User(db.Model):
    INACTIVE = 0
    ACTIVE = 1
    PENDING = 2
    SUSPICIOUS = 3

    TYPES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending'),
        (SUSPICIOUS, 'Suspicious'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    status = db.Column(ChoiceType(TYPES, impl=db.Integer()), default=INACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        # TODO http://marshmallow.readthedocs.org/en/latest/examples.html
        return {
            'id': self.id,
            'email': self.email,
        }


@event.listens_for(User, 'after_insert')
def receive_after_insert(mapper, connection, user):
    # TODO push to a notification/message/notification service
    pass
