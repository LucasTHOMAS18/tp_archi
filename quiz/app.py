import os.path

from flask import Flask
from .extensions import db, migrate
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + mkpath('../quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

from . import models

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
