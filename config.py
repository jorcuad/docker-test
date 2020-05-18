from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    SECRET_KEY = "asdasdasdasd" #environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = 1

    # Database  export SQLALCHEMY_DATABASE_URI=sqlite:///./bd/wardrums.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + path.join(basedir, './bd/wardrums.db')#environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
