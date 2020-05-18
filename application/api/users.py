import datetime
from flask import jsonify, abort
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from application.models.user import User

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('email')
parser.add_argument('password_hash')
parser.add_argument('birthday')
parser.add_argument('user_id')

class UsersAPI(Resource):

    def get(self, id=None):
        if(id == None):
            list = User.query.all()
            return jsonify(json_list=[i.serialize for i in list])

        user = User.query.get(id)

        if user is None:
            abort(404, "User not found.")
        return jsonify(user.serialize)

    def post(self):
        try:
            args = parser.parse_args()
            newUser = User( username=args['username'],
                            email=args['email'],
                            password_hash=args['password_hash'],
                            birthday=datetime.datetime.strptime(args['birthday'], '%d/%m/%Y'))
            newUser.save()
            return jsonify(newUser.serialize)
        except IntegrityError:
            newUser.rollback()
            abort(400, description="Username or account already exists.")

    def put(self):
        try:
            args = parser.parse_args()

            user = User.query.get(int(args['user_id']))

            if user is None:
                abort(404, "User not found.")

            if args['birthday']:
                user.birthday = datetime.datetime.strptime(args['birthday'], '%d/%m/%Y')
            if args['username']:
                if User.query.filter_by(username=args['username']).first() is not None:
                    abort(409, description="Username already exist.")
                user.username = args['username']
            if args['email']:
                if User.query.filter_by(email=args['email']).first() is not None:
                    abort(409, description="Email already exist.")
                user.email = args['email']
            if args['password_hash']:
                user.password_hash = args['password_hash']

            user.update()
            return jsonify(user.serialize)
        except:
            abort(500, description="Error updating user.")

    def delete(self):
        try:
            args = parser.parse_args()
            user = User.query.get(int(args['user_id']))

            if user is None:
                abort(404, "User not found.")

            user.active = False
            user.desactivation_date = datetime.datetime.now()
            user.update()
            return jsonify(user.serialize)
        except:
            abort(500, description="Error deleting user.")
