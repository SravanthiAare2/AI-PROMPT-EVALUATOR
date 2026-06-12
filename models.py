from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    prompt = db.Column(db.Text)
    response = db.Column(db.Text)

    relevance = db.Column(db.Integer)
    clarity = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    consistency = db.Column(db.Integer)
    overall = db.Column(db.Float)