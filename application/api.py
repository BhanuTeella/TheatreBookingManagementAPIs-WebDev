from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from application.database import db
from application.models import User, Song, Album, AlbumSong, Playlist, PlaylistSong, Rating, SongFlag, AlbumFlag
from flask import url_for



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


class SongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('lyrics', type=str)
    parser.add_argument('genre', type=str)
    parser.add_argument('duration', type=int)
    parser.add_argument('creator_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('song_file', type=str)

    def get(self, song_id=None):
        if song_id:
            song = Song.query.get(song_id)
            if song:
                return {
                    'song_id': song.song_id,
                    'name': song.name,
                    'lyrics': song.lyrics,
                    'genre': song.genre,
                    'duration': song.duration,
                    'creator_id': song.creator_id,
                    'song_file_url': url_for('get_song_file', song_id=song.song_id)
                }
            else:
                return {'message': 'Song not found'}, 404
        else:
            return {'songs': list(map(lambda x: x.json(), Song.query.all()))}

    def post(self):
        data = SongResource.parser.parse_args()
        song = Song(name=data['name'], lyrics=data['lyrics'], genre=data['genre'], duration=data['duration'], creator_id=data['creator_id'], song_file=data['song_file'])
        db.session.add(song)
        db.session.commit()
        return song.json(), 201

    def put(self, song_id):
        data = SongResource.parser.parse_args()
        song = Song.query.get(song_id)
        if song:
            song.name = data['name']
            song.lyrics = data['lyrics']
            song.genre = data['genre']
            song.duration = data['duration']
            song.creator_id = data['creator_id']
            song.song_file = data['song_file']
            db.session.commit()
            return song.json()
        else:
            return {'message': 'Song not found'}, 404

    def delete(self, song_id):
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return {'message': 'Song deleted.'}
        else:
            return {'message': 'Song not found'}, 404

class SongsByGenreResource(Resource):
    def get(self, genre):
        songs = Song.query.filter_by(genre=genre).all()
        if songs:
            return {'song_ids': [song.id for song in songs]}
        else:
            return {'message': 'No songs found for this genre'}, 404       

class AlbumResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('artist', type=str)
    parser.add_argument('creator_id', type=int, required=True, help="This field cannot be left blank!")

    def get(self, album_id=None):
        if album_id:
            album = Album.query.get(album_id)
            if album:
                return album.json()
            else:
                return {'message': 'Album not found'}, 404
        else:
            return {'albums': list(map(lambda x: x.json(), Album.query.all()))}

    def post(self):
        data = AlbumResource.parser.parse_args()
        album = Album(name=data['name'], artist=data['artist'], creator_id=data['creator_id'])
        db.session.add(album)
        db.session.commit()
        return album.json(), 201

    def put(self, album_id):
        data = AlbumResource.parser.parse_args()
        album = Album.query.get(album_id)
        if album:
            album.name = data['name']
            album.artist = data['artist']
            album.creator_id = data['creator_id']
            db.session.commit()
            return album.json()
        else:
            return {'message': 'Album not found'}, 404

    def delete(self, album_id):
        album = Album.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()
            return {'message': 'Album deleted.'}
        else:
            return {'message': 'Album not found'}, 404
        


class AlbumSongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('album_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('song_id', type=int, required=True, help="This field cannot be left blank!")

    def get(self, album_id=None, song_id=None):
        if album_id and song_id:
            album_song = AlbumSong.query.filter_by(album_id=album_id, song_id=song_id).first()
            if album_song:
                return album_song.json()
            else:
                return {'message': 'AlbumSong not found'}, 404
        else:
            return {'album_songs': list(map(lambda x: x.json(), AlbumSong.query.all()))}

    def post(self):
        data = AlbumSongResource.parser.parse_args()
        album_song = AlbumSong(album_id=data['album_id'], song_id=data['song_id'])
        db.session.add(album_song)
        db.session.commit()
        return album_song.json(), 201

    def delete(self, album_id, song_id):
        album_song = AlbumSong.query.filter_by(album_id=album_id, song_id=song_id).first()
        if album_song:
            db.session.delete(album_song)
            db.session.commit()
            return {'message': 'AlbumSong deleted.'}
        else:
            return {'message': 'AlbumSong not found'}, 404
        


class PlaylistResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('creator_id', type=int, required=True, help="This field cannot be left blank!")

    def get(self, playlist_id=None):
        if playlist_id:
            playlist = Playlist.query.get(playlist_id)
            if playlist:
                return playlist.json()
            else:
                return {'message': 'Playlist not found'}, 404
        else:
            return {'playlists': list(map(lambda x: x.json(), Playlist.query.all()))}

    def post(self):
        data = PlaylistResource.parser.parse_args()
        playlist = Playlist(name=data['name'], creator_id=data['creator_id'])
        db.session.add(playlist)
        db.session.commit()
        return playlist.json(), 201

    def put(self, playlist_id):
        data = PlaylistResource.parser.parse_args()
        playlist = Playlist.query.get(playlist_id)
        if playlist:
            playlist.name = data['name']
            playlist.creator_id = data['creator_id']
            db.session.commit()
            return playlist.json()
        else:
            return {'message': 'Playlist not found'}, 404

    def delete(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return {'message': 'Playlist deleted.'}
        else:
            return {'message': 'Playlist not found'}, 404
        


class PlaylistSongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('playlist_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('song_id', type=int, required=True, help="This field cannot be left blank!")

    def get(self, playlist_id=None, song_id=None):
        if playlist_id and song_id:
            playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
            if playlist_song:
                return playlist_song.json()
            else:
                return {'message': 'PlaylistSong not found'}, 404
        else:
            return {'playlist_songs': list(map(lambda x: x.json(), PlaylistSong.query.all()))}

    def post(self):
        data = PlaylistSongResource.parser.parse_args()
        playlist_song = PlaylistSong(playlist_id=data['playlist_id'], song_id=data['song_id'])
        db.session.add(playlist_song)
        db.session.commit()
        return playlist_song.json(), 201

    def delete(self, playlist_id, song_id):
        playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
        if playlist_song:
            db.session.delete(playlist_song)
            db.session.commit()
            return {'message': 'PlaylistSong deleted.'}
        else:
            return {'message': 'PlaylistSong not found'}, 404
        

class RatingResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('user_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('rating', type=int, required=True, help="This field cannot be left blank!")

    def get(self, song_id=None, user_id=None):
        if song_id and user_id:
            rating = Rating.query.filter_by(song_id=song_id, user_id=user_id).first()
            if rating:
                return rating.json()
            else:
                return {'message': 'Rating not found'}, 404
        else:
            return {'ratings': list(map(lambda x: x.json(), Rating.query.all()))}

    def post(self):
        data = RatingResource.parser.parse_args()
        rating = Rating(song_id=data['song_id'], user_id=data['user_id'], rating=data['rating'])
        db.session.add(rating)
        db.session.commit()
        return rating.json(), 201

    def put(self, song_id, user_id):
        data = RatingResource.parser.parse_args()
        rating = Rating.query.filter_by(song_id=song_id, user_id=user_id).first()
        if rating:
            rating.rating = data['rating']
            db.session.commit()
            return rating.json()
        else:
            return {'message': 'Rating not found'}, 404

    def delete(self, song_id, user_id):
        rating = Rating.query.filter_by(song_id=song_id, user_id=user_id).first()
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return {'message': 'Rating deleted.'}
        else:
            return {'message': 'Rating not found'}, 404
        


class FlagResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('user_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('flag', type=bool, required=True, help="This field cannot be left blank!")

    def get(self, song_id=None, user_id=None):
        if song_id and user_id:
            flag = Flag.query.filter_by(song_id=song_id, user_id=user_id).first()
            if flag:
                return flag.json()
            else:
                return {'message': 'Flag not found'}, 404
        else:
            return {'flags': list(map(lambda x: x.json(), Flag.query.all()))}

    def post(self):
        data = FlagResource.parser.parse_args()
        flag = Flag(song_id=data['song_id'], user_id=data['user_id'], flag=data['flag'])
        db.session.add(flag)
        db.session.commit()
        return flag.json(), 201

    def put(self, song_id, user_id):
        data = FlagResource.parser.parse_args()
        flag = Flag.query.filter_by(song_id=song_id, user_id=user_id).first()
        if flag:
            flag.flag = data['flag']
            db.session.commit()
            return flag.json()
        else:
            return {'message': 'Flag not found'}, 404

    def delete(self, song_id, user_id):
        flag = Flag.query.filter_by(song_id=song_id, user_id=user_id).first()
        if flag:
            db.session.delete(flag)
            db.session.commit()
            return {'message': 'Flag deleted.'}
        else:
            return {'message': 'Flag not found'}, 404
