from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from hashlib import md5

class Post(db.Model):
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
    is_admin = db.Column(db.Boolean(), default=False)
    last_seen = db.Column(db.DateTime, default=func.now())
    post = db.relationship('Post')
    gallery = db.relationship('Gallery')

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(160))
    img = db.Column(db.String(160), unique=True)
    ext = db.Column(db.String(5))
    date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))