from models.models import db
from models.join import Join
from models.user import UserSchema
from schema.schemas import RoomSchema
import datetime

DAY = 86400

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False, default=4)
    turn_duration = db.Column(db.Integer, nullable=False, default=DAY)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    users = db.relationship('User', secondary="joins", lazy='subquery', load_on_pending=True, backref=db.backref('rooms'))

    @property
    def serialize(self):
        return RoomSchema().dump(self)

    @property
    def serialize_many2many(self):
       return [ item.serialize for item in self.users]

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def __repr__(self):
        return '<Room %r>' % self.room_id
