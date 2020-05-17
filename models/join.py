from models.models import db
from utils.serializer import Serializer
import datetime
from sqlalchemy.orm import relationship, backref

class Join(db.Model):
    __tablename__ = 'joins'
    room_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), primary_key=True)

    @property
    def serialize(self):
       d = Serializer.serialize(self)
       return d

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def __repr__(self):
        return '<Join %r>' % self.id
