from flask import Flask, request, render_template, session
from flask import current_app as app
from application.models import User, Song, Album, AlbumSong, Playlist, PlaylistSong, Rating, SongFlag, AlbumFlag
from flask import request, redirect, url_for, render_template, flash
from .models import User
from flask import send_file, make_response
import io
from .models import db


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
      # Log the user in (add more functionality here)
      flash('Logged in successfully.')
      session['user_id'] = user.user_id
      #redirect to user homepage with user_id
      return redirect(url_for('index', user_id=user.user_id))
    else:
      flash('Invalid email or password.')
  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    # Get the user details from the form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Create a new user instance using the User model
    user = User(username=username, email=email)
    user.set_password(password)
    # Add the new user to the database
    db.session.add(user)
    db.session.commit()

    # Log the user in (add more functionality here)
    flash('Registered successfully.')
    return redirect(url_for('login'))
  return render_template('user_registration.html')


@app.route('/index/<int:user_id>')
def index(user_id):
  #recommend newest 12 songs
  recommended_songs = Song.query.order_by(
      Song.date_created.desc()).limit(12).all()
  genres = Song.query.with_entities(Song.genre).distinct().all()
  genres = [genre[0] for genre in genres]
  return render_template('user_homepage.html',
                         recommended_songs=recommended_songs,
                         genres=genres)


@app.route('/genre/<string:genre_name>')
def genre(genre_name):
  # Fetch the songs from the database using the genre_name
  songs = Song.query.filter_by(genre=genre_name).all()
  if not songs:
    return {'message': 'No songs found for this genre'}, 404
  user_id = session['user_id']
  # Render the results page with the genre name and songs
  return render_template('songlist.html',
                         name=genre_name,
                         songs=songs,
                         user_id=user_id)


@app.route('/search')
def search():
  # Get the search term from the query parameters
  search_term = request.args.get('q', '')
  # Fetch the songs that match the search term
  songs = Song.query.filter(Song.name.contains(search_term)).all()
  user_id = session['user_id']
  # Render the songlist.html template with the search results
  return render_template('songlist.html',
                         name=search_term,
                         songs=songs,
                         user_id=user_id)


@app.route('/songs/<int:song_id>')
def song(song_id):
  # Fetch the song from the database using the song_id
  song = Song.query.get(song_id)
  if song is None:
    return {'message': 'Song not found'}, 404
  user_id = session['user_id']
  # Render the song page with the song details
  return render_template('song.html', song=song, user_id=user_id)


@app.route('/songs/<int:song_id>/file', methods=['GET'])
def get_song_file(song_id):
  song = Song.query.get(song_id)
  if song:
    file_object = io.BytesIO(song.song_file)
    response = make_response(send_file(file_object, mimetype='audio/mpeg'))
    response.headers[
        "Content-Disposition"] = f"attachment; filename={song.name}.mp3"
    return response
  else:
    return {'message': 'Song not found'}, 404


@app.route('/test_models')
def test_models():
    users = User.query.all()
    songs = Song.query.all()
    albums = Album.query.all()
    album_songs = AlbumSong.query.all()
    playlists = Playlist.query.all()
    playlist_songs = PlaylistSong.query.all()
    ratings = Rating.query.all()
    #flags = Flag.query.all()
    return render_template('test_models.html', users=users, songs=songs, albums=albums, album_songs=album_songs, playlists=playlists, playlist_songs=playlist_songs, ratings=ratings, flags=flags)