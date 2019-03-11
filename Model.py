from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    saldo = db.Column(db.Integer)

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value
        return value

    @validates('saldo')
    def validate_saldo(self, key, value):
        assert value > 0
        return value

    def __init__(self, username, email, saldo):
        self.username = username
        self.email = email
        self.saldo = saldo


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email', 'saldo')