__author__ = 'carson.qin'

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.path.dirname(__file__), '../conf.py'))
db = SQLAlchemy(app)

def create_app():
    from Challenge.views import tickets
    app.register_blueprint(tickets, url_prefix='/%s' % app.config.get('VERSION', 'v1'))

    return app
