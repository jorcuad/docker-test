import time
import sqlite3
from flask import g, Flask
app = Flask(__name__)

DATABASE = './bd/chinook.db'

def get_db():
    db = getattr(g, 'chinook', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'chinook', None)
    if db is not None:
        db.close()


@app.route('/status')
def hello():
    return 'I am alive.\n'

@app.route('/connect')
def connect():
    try:
        db = get_db()
        return "Connected"
    except Exception as e:
        print(e)
        return "Error on connection"

@app.route('/')
def index():
    return 'I am alive.\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
