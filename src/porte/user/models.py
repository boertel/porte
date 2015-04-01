from porte import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def json(self):
        # TODO http://marshmallow.readthedocs.org/en/latest/examples.html
        return {
            'id': self.id,
            'email': self.email,
        }
