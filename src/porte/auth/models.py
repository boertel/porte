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

    def create_consumer(self, *args, **kwargs):
        module_name = 'porte.auth.consumers.%sConsumer' % \
            self.name.capitalize()
        path, class_name = module_name.rsplit('.', 1)
        mod = import_module(path)
        obj = getattr(mod, class_name)(**kwargs)
        obj.provider = self
        return obj


class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255))
    verify_token = db.Column(db.String(255))
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
        self.verify_token = self.get_verify_token()

    def get_verify_token(self):
        raise NotImplemented

    def get(self):
        return self.query.filter_by(
            provider=self.provider,
            verify_token=self.get_verify_token())\
            .first()

    def exists(self):
            return self.get is not None
