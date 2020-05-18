from flask import jsonify, abort
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from application.models.room import Room
from application.models.user import User

parser = reqparse.RequestParser()
parser.add_argument('room_id')
parser.add_argument('user_id')

class JoinAPI(Resource):

    def post(self):
        try:
            args = parser.parse_args()
            room = Room.query.get(int(args['room_id']))
            if room is None:
                abort(404, "Room not found.")
            user = User.query.get(int(args['user_id']))
            if user is None:
                abort(404, "User not found.")
            room.users.append(user)
            room.update()

            return room.serialize
        except:
            room.rollback()
            abort(500, description="Error joining room.")

    def delete(self):
        try:
            args = parser.parse_args()
            room = Room.query.get(int(args['room_id']))
            user = User.query.get(int(args['user_id']))

            if room is None:
                abort(404, "Room not found.")
            if user is None:
                abort(404, "User not found.")

            room.users.remove(user)
            room.update()
            return 200
        except:
            abort(500, description="Error deleting room.")
