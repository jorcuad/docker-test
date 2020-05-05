from flask_restful import Resource
from models.user import Users
from flask import jsonify

class UsersAPI(Resource):

    def get(self, id):
        user = Users.query.get(id)
        return jsonify(user.serialize)

class UsersListAPI(Resource):

    def get(self):
        list = Users.query.all()
        return jsonify(json_list=[i.serialize for i in list])
