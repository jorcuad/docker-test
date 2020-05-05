from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort, Response
from flask_restful import Resource, Api
from models.models import db
from schema.schema import Schema
import datetime
from api.users import UsersAPI, UsersListAPI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./bd/wardrums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

VERSION = '/v1'
API = '/api'
USERS_API = API + VERSION + '/users'
ROOMS_API = API + VERSION + '/rooms'

api = Api(app)
api.add_resource(UsersListAPI, USERS_API+'/')
api.add_resource(UsersAPI, USERS_API+'/<id>')

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
