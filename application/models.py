from .database import db
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password

class User(db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)

#Theatre model
class Theatre(db.Model):
    __tablename__ = 'Theatres'
    
    theatre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    capacity = db.Column(db.Integer)
    image_url = db.Column(db.String)

    # one-to-many relationship between Theatre and Show models. one theatre can have many shows
    shows = db.relationship('Show', back_populates='theatre')

# Movie model
class Movie(db.Model):
    __tablename__ = 'Movies'
    
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    tags = db.Column(db.String)
    image_url = db.Column(db.String)

    # one-to-many relationship between Movie and Show models. one movie can be shown in many theatres
    shows = db.relationship('Show', back_populates='movie')

# Show model
class Show(db.Model):
    __tablename__ = 'Shows'
    
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('Theatres.theatre_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.movie_id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    ticket_price = db.Column(db.Float)

    # many-to-one relationship between Show and Theatre models. one theatre can have many shows
    theatre = db.relationship('Theatre', back_populates='shows')

    #  many-to-one relationship between Show and Movie models. one movie can be shown in many theatres
    movie = db.relationship('Movie', back_populates='shows')

# Define the Booking model
class Booking(db.Model):
    __tablename__ = 'Bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    show_id = db.Column(db.Integer, db.ForeignKey('Shows.show_id'))
    num_tickets = db.Column(db.Integer)
    booking_time = db.Column(db.DateTime)

    #  many-to-one relationship between Booking and User models. one user can have many bookings
    user = db.relationship('User', backref='bookings')

    # many-to-one relationship between Booking and Show models. one show can have many bookings
    show = db.relationship('Show', backref='bookings')
    # back_populates vs backref: backpopulate 