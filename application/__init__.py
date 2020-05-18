from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

from application.api.users import UsersAPI
from application.api.rooms import RoomsAPI
from application.api.join import JoinAPI

VERSION = '/v1'
API = '/api'
USERS_API = API + VERSION + '/users'
ROOMS_API = API + VERSION + '/rooms'
JOIN_API = API + VERSION + '/join'

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    api = Api(app)
    api.add_resource(UsersAPI, USERS_API+'/', USERS_API+'/<id>')
    api.add_resource(RoomsAPI, ROOMS_API+'/', ROOMS_API+'/<id>')
    api.add_resource(JoinAPI, JOIN_API)

    with app.app_context():
        db.create_all()  # Create database tables for our data models

        return app
