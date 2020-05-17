from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort, Response
from flask_restful import Resource, Api
from models.models import db
from schema.schema import Schema
import datetime
from api.users import UsersAPI
from api.rooms import RoomsAPI
from api.join import JoinAPI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./bd/wardrums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

VERSION = '/v1'
API = '/api'
USERS_API = API + VERSION + '/users'
ROOMS_API = API + VERSION + '/rooms'
JOIN_API = API + VERSION + '/join'

api = Api(app)
api.add_resource(UsersAPI, USERS_API+'/', USERS_API+'/<id>')
api.add_resource(RoomsAPI, ROOMS_API+'/', ROOMS_API+'/<id>')
api.add_resource(JoinAPI, JOIN_API)

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
