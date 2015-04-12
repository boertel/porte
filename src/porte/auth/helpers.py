from flask import session

from porte import db
from porte.user.models import User


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def consumerize(provider, consumer_data, user_data):
    commit = False
    consumer = provider.get_consumer(**consumer_data)
    if not consumer.exists():
        db.session.add(consumer)
        commit = True
    if not consumer.user:
        user = User.query.filter_by(email=user_data['email']).first()
        if user is None:
            user = User(**user_data)
        consumer.user = user
        db.session.add(user)
        commit = True
    if commit:
        db.session.commit()
    return user
