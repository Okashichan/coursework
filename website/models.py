from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from hashlib import md5
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(1000))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(160))
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(160))
    is_admin = db.Column(db.Boolean())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    notes = db.relationship('Note')


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)