from flask import Flask

from .api import api
from .database import db
from .migrate import migrate
from .sources import sources


def create_app(settings='app.settings.development'):
    app = Flask(__name__)
    app.config.from_object(settings)

    # init crud modules
    sources.init_app(app)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app
