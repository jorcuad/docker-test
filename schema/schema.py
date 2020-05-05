import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('bd/wardrums.db')
        self.create_user_table()
        self.create_room_table()
        self.create_room_users_table()

    def create_user_table(self):
        query = """
        CREATE TABLE if not exists users (
        	user_id INTEGER PRIMARY KEY,
        	username TEXT NOT NULL UNIQUE,
        	email TEXT NOT NULL UNIQUE,
        	password_hash TEXT NOT NULL,
        	birthday TEXT NOT NULL,
        	creation_date TEXT NOT NULL
        );
        """
        self.conn.execute(query)

    def create_room_table(self):
        query = """
        CREATE TABLE if not exists rooms (
           room_id INTEGER PRIMARY KEY,
           capacity INTEGER NOT NULL,
        	 turn_duration INTEGER NOT NULL
        );
        """
        self.conn.execute(query)

    def create_room_users_table(self):
        query = """
        CREATE TABLE if not exists user_rooms(
           user_id INTEGER,
           room_id INTEGER,
           PRIMARY KEY (user_id, room_id),
           FOREIGN KEY (user_id)
              REFERENCES users (user_id)
                 ON DELETE CASCADE
                 ON UPDATE NO ACTION,
           FOREIGN KEY (room_id)
              REFERENCES rooms (room_id)
                 ON DELETE CASCADE
                 ON UPDATE NO ACTION
        );
        """
        self.conn.execute(query)
