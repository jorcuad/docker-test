import datetime
from flask import jsonify, abort
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from application.models.room import Room

parser = reqparse.RequestParser()
parser.add_argument('capacity')
parser.add_argument('turn_duration')
parser.add_argument('room_id')

class RoomsAPI(Resource):

    def get(self, id=None):
        if(id == None):
            list = Room.query.all()
            return jsonify(json_list=[i.serialize for i in list])

        room = Room.query.get(id)

        if room is None:
            abort(404, "Room not found.")
        return jsonify(room.serialize)

    def post(self):
        try:
            args = parser.parse_args()
            newRoom = Room( capacity=args['capacity'],
                            turn_duration=args['turn_duration'])
            newRoom.save()
            return jsonify(newRoom.serialize)
        except:
            newRoom.rollback()
            abort(500, description="Error creating room.")

    def delete(self):
        try:
            args = parser.parse_args()
            room = Room.query.get(int(args['room_id']))

            if room is None:
                abort(404, "Room not found.")

            room.delete()
            return 200
        except:
            abort(500, description="Error deleting room.")
