from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserListResource(Resource):
    
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if user:
            return {'message': 'User already exists'}, 400

        if json_data['saldo'] < 0:
            return {'message': 'Saldo must be a positive value'}, 400

        user = User(
            username=json_data['username'],
            email=json_data['email'],
            saldo=json_data['saldo']
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return {"status": 'success', 'data': result}, 201

class UserResource(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User does not exist'}, 400
        result = user_schema.dump(user).data
        return {'status': 'success', 'data': result}, 200

    def put(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User does not exist'}, 400

        if json_data['saldo'] < 0:
            return {'message': 'Saldo must be a positive value'}, 400

        user.username = data['username']
        user.email = data['email']
        user.saldo = data['saldo']
        db.session.commit()

        result = user_schema.dump(user).data

        return {"status": 'success', 'data': result}, 204

    def patch(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User does not exist'}, 400

        if json_data['saldo'] < 0:
            return {'message': 'Saldo must be a positive value'}, 400

        if 'username' in data:
            user.username = data['username']

        if 'email' in data:
            user.email = data['email']

        if 'saldo' in data:
            user.saldo = data['saldo']

        db.session.commit()

        result = user_schema.dump(user).data

        return {"status": 'success', 'data': result}, 204

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User does not exist'}, 400
        user.delete()
        db.session.commit()

        result = user_schema.dump(user).data

        return {"status": 'success', 'data': result}, 204