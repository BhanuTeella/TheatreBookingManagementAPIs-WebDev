from flask_security import UserMixin, RoleMixin
from sqlalchemy.sql import func
from datetime import datetime

# ... (database setup)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('Users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('Role.id'))
)

class Role(RoleMixin, db.Model):
    __tablename__ = 'Role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(255))

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'roles': [role.name for role in self.roles]
        }

class Song(db.Model):
    __tablename__ = 'Songs'

    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.Text)
    genre = db.Column(db.String)
    duration = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    song_file = db.Column(db.String)  # For storing song file path or data

    def to_dict(self):
        return {
            'song_id': self.song_id,
            'name': self.name,
            'lyrics': self.lyrics,
            'genre': self.genre,
            'duration': self.duration,
            'date_created': self.date_created.isoformat() if isinstance(self.date_created, datetime) else None,
            'creator_id': self.creator_id
        }

class Album(db.Model):
    __tablename__ = 'Albums'

    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def to_dict(self):
        return {
            'album_id': self.album_id,
            'name': self.name,
            'artist': self.artist,
            'creator_id': self.creator_id
        }

class AlbumSong(db.Model):
    __tablename__ = 'AlbumSongs'

    album_id = db.Column(db.Integer, db.ForeignKey('Albums.album_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'), primary_key=True)

    def to_dict(self):
        return {
            'album_id': self.album_id,
            'song_id': self.song_id
        }

class Playlist(db.Model):
    __tablename__ = 'Playlists'

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def to_dict(self):
        return {
            'playlist_id': self.playlist_id,
            'name': self.name,
            'user_id': self.user_id
        }

class PlaylistSong(db.Model):
    __tablename__ = 'PlaylistSongs'

    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlists.playlist_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'), primary_key=True)

    def to_dict(self):
        return {
            'playlist_id': self.playlist_id,
            'song_id': self.song_id
        }

class Rating(db.Model):
    __tablename__ = 'Ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))

    def to_dict(self):
        return {
            'rating_id': self.rating_id,
            'rating': self.rating,
            'user_id': self.user_id,
            'song_id': self.song_id
        }

class SongFlag(db.Model):
    __tablename__ = 'SongFlags'

    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))

    def to_dict(self):
        return {
            'flag_id': self.flag_id,
            'user_id': self.user_id,
            'song_id': self.song_id
        }

class AlbumFlag(db.Model):
    __tablename__ = 'AlbumFlags'

    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('Albums.album_id'))

    def to_dict(self):
        return {
            'flag_id': self.flag_id,
            'user_id': self.user_id,
            'album_id': self.album_id
        }