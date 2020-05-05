from models import db

DAY = 86400

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False, default=4)
    duration = db.Column(db.Integer, nullable=False, default=DAY)

    def __repr__(self):
        return '<Room %r>' % self.id
