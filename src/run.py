from porte import app, db

from porte.auth.models import *
from porte.user.models import *
from porte.auth.views import *


if __name__ == '__main__':
    db.create_all()
    app.run()
