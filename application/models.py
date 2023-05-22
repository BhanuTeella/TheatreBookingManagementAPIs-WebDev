from .database import db
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

class Theatre(db.Model):
    __tablename__ = 'theatres'
    
    theatre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    capacity = db.Column(db.Integer)

    shows = db.relationship('Show', back_populates='theatre')

class Movie(db.Model):
    __tablename__ = 'movies'
    
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    tags = db.Column(db.String)

    shows = db.relationship('Show', back_populates='movie')

class Show(db.Model):
    __tablename__ = 'shows'
    
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_time = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    show_price = db.Column(db.Float)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatres.theatre_id'))
    
    movie = db.relationship('Movie', back_populates='shows')
    theatre = db.relationship('Theatre', back_populates='shows')

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'))
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatres.theatre_id'))
    
    user = db.relationship('User')
    show = db.relationship('Show')
    theatre = db.relationship('Theatre')