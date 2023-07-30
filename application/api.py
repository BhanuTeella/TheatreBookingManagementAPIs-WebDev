from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from application.database import db
from application.models import User, Theatre, Movie, Show, Booking



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




class TheatreResource(Resource):
    def get(self, theatre_id):
        theatre = Theatre.query.get(theatre_id)
        if theatre:
            return {
                'theatre_id': theatre.theatre_id,
                'name': theatre.name,
                'address': theatre.location,
                'capacity': theatre.capacity,
                'image_url': theatre.image_url
            }
        else:
            return {'message': 'Theatre not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        parser.add_argument('capacity', type=int, required=True)
        parser.add_argument('image_url', type=str, required=True)
        args = parser.parse_args()

        theatre = Theatre(name=args['name'], location=args['location'], capacity=args['capacity'])
        db.session.add(theatre)
        db.session.commit()

        return {'message': 'Theatre created', 'theatre_id': theatre.theatre_id}, 201

    def delete(self, theatre_id):
        theatre = Theatre.query.get(theatre_id)
        if theatre:
            db.session.delete(theatre)
            db.session.commit()
            return {'message': 'Theatre deleted'}
        else:
            return {'message': 'Theatre not found'}, 404

class MovieResource(Resource):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            return {
                'movie_id': movie.movie_id,
                'name': movie.name,
                'rating': movie.rating,
                'tags': movie.tags
            }
        else:
            return {'message': 'Movie not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('rating', type=float, required=True)
        parser.add_argument('tags', type=str, required=True)
        args = parser.parse_args()

        movie = Movie(name=args['name'], rating=args['rating'], tags=args['tags'])
        db.session.add(movie)
        db.session.commit()

        return {'message': 'Movie created', 'movie_id': movie.movie_id}, 201

    def put(self, movie_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('rating', type=float, required=True)
        parser.add_argument('tags', type=str, required=True)
        args = parser.parse_args()

        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = args['name']
            movie.rating = args['rating']
            movie.tags = args['tags']
            db.session.commit()
            return {'message': 'Movie updated', 'movie_id': movie.movie_id}
        else:
            return {'message': 'Movie not found'}, 404

    def delete(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted'}
        else:
            return {'message': 'Movie not found'}, 404

class ShowResource(Resource):
    def get(self, show_id):
        show = Show.query.get(show_id)
        if show:
            return {
                'show_id': show.show_id,
                'show_time': show.show_time,
                'movie_id': show.movie_id,
                'ticket_price': show.ticket_price,
                'theatre_id': show.theatre_id
            }
        else:
            return {'message': 'Show not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('show_time', type=str, required=True)
        parser.add_argument('movie_id', type=int, required=True)
        parser.add_argument('ticket_price', type=float, required=True)
        parser.add_argument('theatre_id', type=int, required=True)
        args = parser.parse_args()

        show = Show(show_time=args['show_time'], movie_id=args['movie_id'], ticket_price=args['ticket_price'],
                    theatre_id=args['theatre_id'])
        db.session.add(show)
        db.session.commit()

        return {'message': 'Show created', 'show_id': show.show_id}, 201
    
    def put(self, show_id):
        parser = reqparse.RequestParser()
        parser.add_argument('show_time', type=str, required=True)
        parser.add_argument('movie_id', type=int, required=True)
        parser.add_argument('ticket_price', type=float, required=True)
        parser.add_argument('theatre_id', type=int, required=True)
        args = parser.parse_args()

        show = Show.query.get(show_id)
        if show:
            show.show_time = args['show_time']
            show.movie_id = args['movie_id']
            show.ticket_price = args['ticket_price']
            show.theatre_id = args['theatre_id']
            db.session.commit()
            return {'message': 'Show updated', 'show_id': show.show_id}
        else:
            return {'message': 'Show not found'}, 404
        
    def delete(self, show_id):
        show = Show.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return {'message': 'Show deleted'}
        else:
            return {'message': 'Show not found'}, 404

class BookingResource(Resource):
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            return {
                'booking_id': booking.booking_id,
                'user_id': booking.user_id,
                'show_id': booking.show_id,
                'theatre_id': booking.theatre_id
            }
        else:
            return {'message': 'Booking not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('show_id', type=int, required=True)
        parser.add_argument('theatre_id', type=int, required=True)
        args = parser.parse_args()

        booking = Booking(user_id=args['user_id'], show_id=args['show_id'], theatre_id=args['theatre_id'])
        db.session.add(booking)
        db.session.commit()

        return {'message': 'Booking created', 'booking_id': booking.booking_id}, 201

    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {'message': 'Booking deleted'}
        else:
            return {'message': 'Booking not found'}, 404

