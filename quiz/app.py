# FILE: quiz/app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Fonction utilitaire pour construire les chemins relatifs
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + mkpath('../quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
