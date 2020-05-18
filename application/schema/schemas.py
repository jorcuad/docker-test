from marshmallow import Schema, fields

class RoomSchema(Schema):
    id = fields.Int()
    capacity = fields.Int()
    turn_duration = fields.Int()
    creation_date = fields.DateTime()
    users = fields.Nested(lambda: UserSchema(only=("id", "username")), many = True, dump_only = True)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    email = fields.Email()
    birthday = fields.DateTime()
    creation_date = fields.DateTime()
    active = fields.Boolean()
    desactivation_date = fields.DateTime()
    rooms = fields.Nested(RoomSchema(only=("id", "capacity", "turn_duration", "creation_date")), many = True, dump_only = True)
