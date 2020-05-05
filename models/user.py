from models.models import db
from utils.serializer import Serializer
import datetime

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    @property
    def serialize(self):
       d = Serializer.serialize(self)
       del d['password_hash']
       return d

    def __repr__(self):
        return '<User %r>' % self.username
