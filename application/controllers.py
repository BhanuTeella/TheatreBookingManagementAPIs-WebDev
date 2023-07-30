from flask import Flask, request, render_template
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from application.models import User, Theatre, Movie, Show, Booking

@app.route('/')
def test_models():
    users = User.query.all()
    theatres = Theatre.query.all()
    movies = Movie.query.all()
    shows = Show.query.all()
    bookings = Booking.query.all()

    return render_template('test_models.html', users=users, theatres=theatres, movies=movies, shows=shows, bookings=bookings)