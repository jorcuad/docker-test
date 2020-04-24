CREATE TABLE if not exists users (
	user_id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	birthday TEXT NOT NULL,
	registration TEXT NOT NULL
);

CREATE TABLE if not exists rooms (
   room_id INTEGER PRIMARY KEY,
   capacity INTEGER NOT NULL,
	 turn_duration INTEGER NOT NULL
);

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
