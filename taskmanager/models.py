from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # Schema model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)