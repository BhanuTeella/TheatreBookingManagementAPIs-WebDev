from flask import Flask, request, render_template
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from application.models import User, Theatre, Movie, Show, Booking

@app.route('/')
def test_models():
    users = User.query.all()
    theatres = Theatre.query.all()
    movies = Movie.query.all()
    shows = Show.query.filter_by(theatre_id=1).all()
    bookings = Booking.query.filter_by(user_id=1).all()

    return render_template('test_models.html', users=users, theatres=theatres, movies=movies, shows=shows, bookings=bookings)