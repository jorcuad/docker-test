import time
import sqlite3
import datetime
import secrets
from flask_sqlalchemy import SQLAlchemy

from flask import g, Flask, Response, abort, request, jsonify
app = Flask(__name__)

DATABASE = './bd/wardrums.db'
DATABASE_NAME ='wardrums'
DATABASE_SCHEMA ='./bd/wardrums.sql'
VERSION = '/v1'
API = '/api'
USERS_API = API + VERSION + '/users'
ROOMS_API = API + VERSION + '/rooms'

def get_db():
    db = getattr(g, DATABASE_NAME, None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#TODO REMOVE IN PROD
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

#TODO REMOVE IN PROD
@app.route('/reset', methods=['GET'])
def erase_db():
    with app.app_context():
        try:
            db = get_db()
            db.cursor().execute('DELETE FROM rooms')
            db.cursor().execute('DELETE FROM users')
            db.cursor().execute('DELETE FROM user_rooms')
            db.commit()
            return Response(status=201)
        except Exception as e:
            abort(500, description=e)

#TODO REMOVE IN PROD
@app.route('/dummy', methods=['GET'])
def reset_testData():
    try:
        init_testData()
        return Response(status=201)
    except Exception as e:
        abort(500, description=e)

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

@app.route('/status', methods=['GET'])
def hello():
    return 'I am alive.\n'

@app.route('/connect', methods=['GET'])
def connect():
    try:
        db = get_db()
        return "Connected"
    except Exception as e:
        print(e)
        return "Error on connection"

@app.route(USERS_API+'/create', methods=['POST'])
def create_user():
    try:
        if not request.json or not request.is_json:
            abort(400, description="Bad request.")
        data = request.get_json()
        user = (secrets.randbelow(999999), data['name'], datetime.datetime.now(), data['mail'], data['password'], data['birthday'])
        db = get_db()
        db.cursor().execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", user)
        db.commit()
        return Response(status=201)
    except Exception as e:
        abort(500, description="Error creating user.")

@app.route(USERS_API+'/update', methods=['POST'])
def update_user():
    return "Not implemented yet."

@app.route(USERS_API, methods=['GET'])
def list_users():
    try:
        db = get_db()
        users_cursor = db.cursor().execute("SELECT * FROM users")
        users = []
        for user_cursor in users_cursor.fetchall():
            user = {'name': user_cursor[1] ,'mail': user_cursor[3], 'id': user_cursor[0], 'birthday': user_cursor[2]}
            users.append(user)
        return jsonify(users)
    except Exception as e:
        abort(500, description="Error retrieving users.")

@app.route(ROOMS_API, methods=['GET'])
def list_rooms():
    try:
        db = get_db()
        rooms_cursor = db.cursor().execute("SELECT * FROM rooms")
        rooms = []
        for room_cursor in rooms_cursor.fetchall():
            room = {'capacity': room_cursor[1] ,'duration': room_cursor[2], 'id': room_cursor[0]}
            rooms.append(room)
        return jsonify(rooms)
    except Exception as e:
        abort(500, description="Error retrieving rooms.")

@app.route(ROOMS_API+"/<roomid>", methods=['GET'])
def list_room_joins(roomid):
    try:
        db = get_db()
        joins_cursor = db.cursor().execute("SELECT * FROM user_rooms where room_id=? ", roomid)
        joined = []
        for join in joins_cursor.fetchall():
            joined.append(join[0])
        room_cursor = db.cursor().execute("SELECT * FROM rooms where room_id=? ", roomid)
        roomraw = room_cursor.fetchone()

        room = {'joined': joined, 'id': roomraw[0], 'capacity': roomraw[1], 'duration': roomraw[2]}

        return jsonify(room)
    except Exception as e:
        abort(500, description=e)

@app.route(ROOMS_API+'/create', methods=['POST'])
def create_room():
    try:
        if not request.json or not request.is_json:
            abort(400, description="Bad request.")
        data = request.get_json()
        room = (secrets.randbelow(999999), data['capacity'], data['duration'] )
        db = get_db()
        db.cursor().execute("INSERT INTO rooms VALUES(?, ?, ?)", room)
        db.commit()
        return Response(status=201)
    except Exception as e:
        abort(500, description="Error creating room.")

@app.route(ROOMS_API+'/join', methods=['POST'])
def join_room():
    try:
        if not request.json or not request.is_json:
            abort(400, description="Bad request.")
        data = request.get_json()
        join = (data['user_id'], data['room_id'])
        db = get_db()
        db.cursor().execute("INSERT INTO user_rooms VALUES(?, ?)", join)
        db.commit()
        return Response(status=201)
    except Exception as e:
        abort(500, description="Error joining room.")

@app.route('/')
def index():
    return 'I am alive.\n'

if __name__ == '__main__':
    init_db()
    #init_testData()
    app.run(host='0.0.0.0')
