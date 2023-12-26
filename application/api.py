from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from application.database import db
from application.models import User



class UserResource(Resource):
    def get(self, user_id=None):
        user = User.query.get(user_id)
        if user:
            return {
                'user_id': user.user_id,
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
        else:
            return {'message': 'User not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        user = User(username=args['username'], password=args['password'], email=args['email'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created', 'user_id': user.user_id}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        user = User.query.get(user_id)
        if user:
            user.username = args['username']
            user.password = args['password']
            user.email = args['email']
            db.session.commit()
            return {'message': 'User updated', 'user_id': user.user_id}
        else:
            return {'message': 'User not found'}, 404
        
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        else:
            return {'message': 'User not found'}, 404
