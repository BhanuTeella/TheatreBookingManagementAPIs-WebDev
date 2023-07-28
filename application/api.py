from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
api = Api(app)



class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {
                'user_id': user.user_id,
                'username': user.username,
                'password': user.password
            }
        else:
            return {'message': 'User not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created', 'user_id': user.user_id}, 201

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
                'location': theatre.location,
                'capacity': theatre.capacity
            }
        else:
            return {'message': 'Theatre not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('capacity', type=int, required=True)
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
                'show_price': show.show_price,
                'theatre_id': show.theatre_id
            }
        else:
            return {'message': 'Show not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('show_time', type=str, required=True)
        parser.add_argument('movie_id', type=int, required=True)
        parser.add_argument('show_price', type=float, required=True)
        parser.add_argument('theatre_id', type=int, required=True)
        args = parser.parse_args()

        show = Show(show_time=args['show_time'], movie_id=args['movie_id'], show_price=args['show_price'],
                    theatre_id=args['theatre_id'])
        db.session.add(show)
        db.session.commit()

        return {'message': 'Show created', 'show_id': show.show_id}, 201

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

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(TheatreResource, '/theatres', '/theatres/<int:theatre_id>')
api.add_resource(MovieResource, '/movies', '/movies/<int:movie_id>')
api.add_resource(ShowResource, '/shows', '/shows/<int:show_id>')
api.add_resource(BookingResource, '/bookings', '/bookings/<int:booking_id>')

if __name__ == '__main__':
    app.run()
