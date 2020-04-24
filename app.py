import time
import sqlite3
import datetime

from flask import g, Flask
app = Flask(__name__)

DATABASE = './bd/wardrums.db'
DATABASE_NAME ='wardrums'
DATABASE_SCHEMA ='./bd/wardrums.sql'

def get_db():
    db = getattr(g, DATABASE_NAME, None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_testData():
    with app.app_context():
        db = get_db()
        users = [
                (1, "Anacleto", datetime.date(2017, 1, 2), "anacleto@agentesecreto.com", "02ed37628326d139ccdf0ca0b25812781bb94e50a7cfea22d22acdfd10ad44a1", datetime.date(2017, 1, 2)),
                (2, "Mortadelo", datetime.date(2018, 3, 4), "mortadelo@latia.com", "912195d37c93864efd93d9a95ba328da40fe193a57d47c380c754436fec28e2b", datetime.date(2018, 3, 4)),
                (3, "Filemon", datetime.date(2015, 3, 4), "filemon@latia.com", "cf0fe955e9c2a947db37741ba9ca6fb2914c76c92229a61e9729b44bdec5f75b",  datetime.date(2015, 3, 4)),
                (4, "SuperEñe", datetime.date(2012, 3, 4), "superene@supertres.es", "c7c874ab587cd34bceb6c127920661d5f79f8351e4045e7d4192918deb4521a1", datetime.date(2012, 3, 4))
                ]
        rooms = [
                (1, 4, 16000),
                (2, 7, 200)
                ]
        user_rooms = [
                    (1,1),
                    (1,2),
                    (2,2),
                    (3,1),
                    (4,1),
                    (4,2)
                    ]
        db.cursor().executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", users)
        db.cursor().executemany("INSERT INTO rooms VALUES(?, ?, ?)", rooms)
        db.cursor().executemany("INSERT INTO user_rooms VALUES(?, ?)", user_rooms)
        db.commit()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(DATABASE_SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, DATABASE_NAME, None)
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
    init_db()
    init_testData()
    app.run(host='0.0.0.0')
