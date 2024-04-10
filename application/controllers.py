from flask import Flask, request, render_template, session
from flask import current_app as app
from application.models import User, Song, Album, AlbumSong, Playlist, PlaylistSong, SongRating,AlbumRating, SongFlag, AlbumFlag, Role
from flask import request, redirect, url_for, render_template, flash
from .models import User
from flask import send_file, make_response
import io
from .models import db
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os
import uuid
import re
from flask_security import current_user
from flask import redirect, url_for



@app.route('/')
def home():
  return render_template('index.html')



@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password) and 'admin' in [role.name for role in user.roles]:
      return redirect(url_for('admin_dashboard'))
    else:
      flash('Invalid email or password, or you are not an admin.')
      return redirect(url_for('admin_login'))

  return render_template('admin_login.html')

'''@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    # Get the user details from the form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Generate a unique fs_uniquifier
    fs_uniquifier = str(uuid.uuid4())
    # Create a new user instance using the User model
    user = User(username=username, email=email, fs_uniquifier=fs_uniquifier, active=1)  # Set active to True
    user.set_password(password)
    # Assign a default role to the user
    default_role = Role.query.get(3)  # Get the role with id 3
    if default_role:
        user.roles.append(default_role)
    else:
        flash('Default role not found. Please contact the administrator.')
        return redirect(url_for('register'))
    # Add the new user to the database
    db.session.add(user)
    db.session.commit()

    # Log the user in (add more functionality here)
    flash('Registered successfully.')
    return redirect(url_for('login'))
  return render_template('user_registration.html')'''


@app.route('/index')
def index():
  user_id=current_user.id
  #recommend newest 12 songs
  recommended_songs = Song.query.order_by(
      Song.date_created.desc()).limit(12).all()
  genres = Song.query.with_entities(Song.genre).distinct().all()
  genres = [genre[0] for genre in genres]
  playlists = Playlist.query.all()
  albums = Album.query.all()
  return render_template('user_homepage.html',
                         recommended_songs=recommended_songs,
                         genres=genres, playlists=playlists, albums=albums)


@app.route('/genre/<string:genre_name>')
def genre(genre_name):
  # Fetch the songs from the database using the genre_name
  songs = Song.query.filter_by(genre=genre_name).all()
  if not songs:
    return {'message': 'No songs found for this genre'}, 404
  user_id = current_user.id
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
  user_id = current_user.id
  # Render the songlist.html template with the search results
  return render_template('songlist.html',
                         name=search_term,
                         songs=songs,
                         user_id=user_id)
'''

@app.route('/songs/<int:song_id>')
def song(song_id):
  # Fetch the song from the database using the song_id
  song = Song.query.get(song_id)
  if song is None:
    return {'message': 'Song not found'}, 404
  user_id = current_user.id
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
'''
@app.route('/creator_account')
def creator_account():
  user_id = current_user.id
  user = User.query.get(user_id)
  if 'creator' not in [role.name for role in user.roles]:
    return render_template('register_as_creator.html')
  else:
    songs = Song.query.filter_by(creator_id=user_id).all()
    if songs:
      albums = Album.query.filter_by(creator_id=user_id).all()
      ratings = [song.rating for song in songs]
      return render_template('creator_dashboard.html', songs=songs, albums=albums, ratings=ratings)
    else:
      return render_template('start_creating.html')
    

@app.route('/become_creator', methods=['POST'])
def become_creator():
  user_id = current_user.id
  user = User.query.get(user_id)
  creator_role = Role.query.filter_by(name='creator').first()
  user.roles.append(creator_role)
  db.session.commit()
  return redirect(url_for('creator_account'))


@app.route('/upload_song', methods=['GET', 'POST'])
def upload_song():
  if request.method == 'POST':
    # Get song details from the form
    name = request.form['name']
    lyrics = request.form['lyrics']
    genre = request.form['genre']
    duration = request.form['duration']
    song_file = request.files['song_file']

    # Perform validation
    if not name or not lyrics or not genre or not duration or not song_file:
      flash('All fields are required.')
      return redirect(request.url)

    # Check the file format
    if not '.' in song_file.filename or not song_file.filename.rsplit('.', 1)[1].lower() in ['mp3']:
      flash('Invalid file format. Only MP3 files are allowed.')
      return redirect(request.url)

    # Sanitize the song name to use as a filename
    safe_name = re.sub(r'[\\/*?:"<>|]', '', name)  # Remove invalid characters
    safe_name = safe_name.replace(' ', '_')  # Replace spaces with underscores

    # Append a unique identifier to the filename to avoid overwriting files
    ext = song_file.filename.rsplit('.', 1)[1].lower()  # Get the file extension
    filename = f"{safe_name}_{uuid.uuid4().hex}.{ext}"

    # Ensure the directory exists
    directory = 'path/to/save/files'
    os.makedirs(directory, exist_ok=True)

    # Save the file
    song_file.save(os.path.join(directory, filename))

    # Create a new song instance using the Song model
    song = Song(name=name, lyrics=lyrics, genre=genre, duration=duration, 
          date_created=datetime.now(timezone.utc), creator_id=current_user.id, 
          song_file=filename)
    # Add the new song to the database
    db.session.add(song)
    db.session.commit()

    flash('Song uploaded successfully.')
    return redirect(url_for('upload_song'))
  genres = Song.query.with_entities(Song.genre).distinct().all()
  genres = [genre[0] for genre in genres]

  return render_template('upload_song.html',genres=genres)


@app.route('/test_models')
def test_models():
    users = User.query.all()
    songs = Song.query.all()
    albums = Album.query.all()
    album_songs = AlbumSong.query.all()
    playlists = Playlist.query.all()
    playlist_songs = PlaylistSong.query.all()
    ratings = Rating.query.all()
    return render_template('test_models.html', users=users, songs=songs, albums=albums, album_songs=album_songs, playlists=playlists, playlist_songs=playlist_songs, ratings=ratings)


'''@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    print('inside post')  # Debug line  
    email = request.form['email']
    password = request.form['password']
    print(f'Form data: {request.form}')  # Debug line
    print(f'Request data: {request.data}')  # Debug line
    print(f'Request JSON: {request.json}')  # Debug line


    user = User.query.filter_by(email=email).first()
    print(f'User: {user}')  # Debug line
    if user:
      print(f'Hashed password in DB: {user.password}')  # Debug line
      print(f'Hashed provided password: {user.hash_password(password)}')  # Debug line
      print(f'Password check: {user.check_password(password)}')  # Debug line
    if user and user.check_password(password):
      print(user.id)
      print('logged in')
      # Log the user in (add more functionality here)
      flash('Logged in successfully.')
      session['user_id'] = user.id
      #redirect to user homepage with user_id
      return redirect(url_for('index', user_id=user.id))
    else:
      flash('Invalid email or password.')
  return redirect(url_for('login'))
'''
