from marshmallow import Schema, fields

class RoomSchema(Schema):
    room_id = fields.Int()
    capacity = fields.Int()
    turn_duration = fields.Int()
    creation_date = fields.DateTime()
    users = fields.Nested(lambda: UserSchema(only=("user_id", "username")))

class UserSchema(Schema):
    user_id = fields.Int()
    username = fields.String()
    email = fields.Email()
    birthday = fields.DateTime()
    creation_date = fields.DateTime()
    active = fields.Boolean()
    desactivation_date = fields.DateTime()
    rooms = fields.Nested(RoomSchema(only=("room_id", "capacity", "turn_duration", "creation_date")))
