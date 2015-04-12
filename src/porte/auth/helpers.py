from flask import session

from porte import db
from porte.user.models import User
from porte.auth.models import Consumer
from porte.auth.exceptions import AlreadyExistsException


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def register(provider, uid, params, user_data):
    consumer, created = Consumer.get_or_create(provider=provider,
                                               uid=uid,
                                               params=params)
    if not created:
        raise AlreadyExistsException('Consumer already exists')
    if not consumer.user:
        email = user_data['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(**user_data)
        # association
        consumer.user = user
        db.session.add(user)
        db.session.commit()
    return consumer.user


def login(provider, uid, params):
    consumer = Consumer.query.filter_by(provider=provider, uid=uid).first()
    if consumer and consumer.user and consumer.is_valid(params):
        return consumer.user


def register_or_login(provider, uid, params, user_data):
    try:
        user = register(provider, uid, params, user_data)
        new = True
    except AlreadyExistsException:
        user = login(provider, uid, params)
        new = False
    return user, new
