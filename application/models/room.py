import datetime
from sqlalchemy.orm import relationship

from application import db
from application.schema.schemas import RoomSchema

DAY = 86400

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

association_table = db.Table('joins', db.metadata,
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False, default=4)
    turn_duration = db.Column(db.Integer, nullable=False, default=DAY)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    users = relationship("User",
                    secondary=association_table,
                    backref="rooms")

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
