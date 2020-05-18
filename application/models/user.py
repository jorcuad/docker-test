import datetime

from application import db
from application.schema.schemas import UserSchema

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    active = db.Column(db.Boolean, nullable=False, default=True)
    desactivation_date = db.Column(db.DateTime)

    @property
    def serialize(self):
       return UserSchema().dump(self)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.username
