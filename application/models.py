from .database import db
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password
from sqlalchemy.sql import func

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('Users.user_id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('Role.role_id')))

class Role(RoleMixin, db.Model):
    __tablename__ = 'Role'
    
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Song(db.Model):
    __tablename__ = 'Songs'
    
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.Text)
    genre = db.Column(db.String)
    duration = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    song_file_url = db.Column(db.String)

class Album(db.Model):
    __tablename__ = 'Albums'
    
    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class AlbumSong(db.Model):
    __tablename__ = 'AlbumSongs'
    
    album_id = db.Column(db.Integer, db.ForeignKey('Albums.album_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'), primary_key=True)

class Playlist(db.Model):
    __tablename__ = 'Playlists'
    
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class PlaylistSong(db.Model):
    __tablename__ = 'PlaylistSongs'
    
    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlists.playlist_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'), primary_key=True)

class Rating(db.Model):
    __tablename__ = 'Ratings'
    
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))

class SongFlag(db.Model):
    __tablename__ = 'SongFlags'
    
    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))

class AlbumFlag(db.Model):
    __tablename__ = 'AlbumFlags'
    
    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    album_id = db.Column(db.Integer, db.ForeignKey('Albums.album_id'))

