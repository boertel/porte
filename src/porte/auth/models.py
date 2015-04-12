import json
from importlib import import_module

from porte import db
from porte.utils import JSONAlchemy


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    _params = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity': 'provider',
        'polymorphic_on': name
    }

    @property
    def params(self):
        return json.loads(self._params)

    @params.setter
    def params(self, value):
        self._params = json.dumps(value)


def get_consumer_class(provider_name):
    module_name = 'porte.auth.consumers.%sConsumer' % \
        provider_name.capitalize()
    path, class_name = module_name.rsplit('.', 1)
    mod = import_module(path)
    return getattr(mod, class_name)


class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255))
    params = db.Column(JSONAlchemy(db.Text(600)))
    provider_id = db.Column(
        db.Integer, db.ForeignKey('provider.id', ondelete='CASCADE')
    )
    provider = db.relationship('Provider')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)

    @classmethod
    def get_or_create(cls, provider, uid, params=None):
        model = get_consumer_class(provider.name)

        instance = db.session.query(model).filter_by(provider=provider, uid=uid)\
            .first()
        if instance:
            return instance, False
        else:
            instance = model(provider=provider, uid=uid, params=params)
            db.session.add(instance)
            db.session.commit()
            return instance, True
