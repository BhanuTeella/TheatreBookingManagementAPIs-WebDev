from flask_restful import Resource, reqparse
from flask_security import login_required, roles_required, current_user
from flask import url_for, jsonify
from io import BytesIO
from flask import send_file
from flask import request
from application.database import db
from application.models import User,Role, Song, Album, AlbumSong, Playlist, PlaylistSong,SongRating,AlbumRating, SongFlag, AlbumFlag


# ... (other imports if needed)

class AdminDashboardResource(Resource):
    @login_required
    @roles_required('admin')
    def get(self):
        # Get statistics for admin dashboard
        total_users = User.query.count()
        total_creators = User.query.filter(User.roles.any(name='creator')).count()
        total_albums = Album.query.count()
        total_songs = Song.query.count()

        # You can add more statistics as needed

        return jsonify({
            'total_users': total_users,
            'total_creators': total_creators,
            'total_albums': total_albums,
            'total_songs': total_songs
        })

class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('is_creator', type=bool, default=False)  # Optional field for creator signup
        args = parser.parse_args()

        # Check if user already exists
        if User.query.filter_by(email=args['email']).first():
            return {'message': 'User with that email already exists'}, 400

        # Create user
        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])  # Use Flask-Security's password hashing

        # Assign role (creator or general user)
        if args['is_creator']:
            creator_role = Role.query.filter_by(name='creator').first()
            user.roles.append(creator_role)

        db.session.add(user)
        db.session.commit()

        return {'message': 'User registered', 'user_id': user.id}, 201

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username_or_email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        # Authenticate user (use Flask-Security's authentication methods)
        user = User.query.filter(
            (User.username == args['username_or_email']) | (User.email == args['username_or_email'])
        ).first()

        if user and user.check_password(args['password']):
            # Generate token or handle session (depending on your authentication method)
            # ... (token/session logic)

            return {'message': 'User logged in', 'token': token}, 200  # Or return session data
        else:
            return {'message': 'Invalid credentials'}, 401

class ProfileResource(Resource):
    @login_required
    def get(self):
        user = current_user  # Get the currently logged-in user
        return jsonify(user.to_dict())

    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        # ... (add arguments for other fields you want to update)
        args = parser.parse_args()

        user = current_user

        # Update user profile fields based on args
        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        # ... (update other fields)

        db.session.commit()
        return jsonify(user.to_dict())

class SongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('lyrics', type=str)
    parser.add_argument('genre', type=str)
    parser.add_argument('duration', type=int)
    parser.add_argument('song_file', type=str)  # For song file upload

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to create songs
    def post(self):
        args = SongResource.parser.parse_args()

        # Create song
        song = Song(
            name=args['name'],
            lyrics=args['lyrics'],
            genre=args['genre'],
            duration=args['duration'],
            creator_id=current_user.id,
            song_file=args['song_file']  # Handle song file upload and storage
        )

        db.session.add(song)
        db.session.commit()

        return jsonify(song.to_dict()), 201

    @login_required
    def get(self, song_id):
        song = Song.query.get(song_id)
        if song:
            return jsonify(song.to_dict())
        else:
            return {'message': 'Song not found'}, 404

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to update songs
    def put(self, song_id):
        args = SongResource.parser.parse_args()

        song = Song.query.get(song_id)
        if song:
            # Update song fields based on args
            if args['name']:
                song.name = args['name']
            if args['lyrics']:
                song.lyrics = args['lyrics']
            if args['genre']:
                song.genre = args['genre']
            if args['duration']:
                song.duration = args['duration']
            if args['song_file']:
                song.song_file = args['song_file']

            db.session.commit()

            return jsonify(song.to_dict())
        else:
            return {'message': 'Song not found'}, 404

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to delete songs
    def delete(self, song_id):
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return {'message': 'Song deleted'}
        else:
            return {'message': 'Song not found'}, 404

class SongFileResource(Resource):
    @login_required
    def get(self, song_id):
        song = Song.query.get(song_id)
        if song and song.song_file:
            return send_file(BytesIO(song.song_file), mimetype='audio/mpeg')
        else:
            return {'message': 'No song file found'}, 404

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to upload files
    def post(self, song_id):
        song = Song.query.get(song_id)
        if song:
            # Handle file upload logic and store the file in the database
            file = request.files['file']
            song.song_file = file.read()
            db.session.commit()
            return {'message': 'File uploaded successfully'}
        else:
            return {'message': 'Song not found'}, 404


class AlbumResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('artist', type=str)
    parser.add_argument('creator_id', type=int, required=True, help="This field cannot be left blank!")
    
    @login_required
    def get(self, album_id=None):
        if album_id:
            album = Album.query.get(album_id)
            if album:
                return jsonify(album.to_dict())
            else:
                return jsonify({'message': 'Album not found'}), 404
        else:
            return jsonify({'albums': [album.to_dict() for album in Album.query.all()]})
    
    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to create albums
    def post(self):
        data = AlbumResource.parser.parse_args()
        album = Album(name=data['name'], artist=data['artist'], creator_id=data['creator_id'])
        db.session.add(album)
        db.session.commit()
        return jsonify(album.to_dict()), 201

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to create albums
    def put(self, album_id):
        data = AlbumResource.parser.parse_args()
        album = Album.query.get(album_id)
        if album:
            album.name = data['name']
            album.artist = data['artist']
            album.creator_id = data['creator_id']
            db.session.commit()
            return jsonify(album.to_dict())
        else:
            return jsonify({'message': 'Album not found'}), 404

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to delete albums
    def delete(self, album_id):
        album = Album.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()
            return jsonify({'message': 'Album deleted.'})
        else:
            return jsonify({'message': 'Album not found'}), 404

class PlaylistResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)

    @login_required
    def post(self):
        args = PlaylistResource.parser.parse_args()

        # Create playlist
        playlist = Playlist(name=args['name'], user_id=current_user.id)

        db.session.add(playlist)
        db.session.commit()

        return jsonify(playlist.to_dict()), 201

    @login_required
    def get(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if playlist:
            return jsonify(playlist.to_dict())
        else:
            return {'message': 'Playlist not found'}, 404

    @login_required
    def put(self, playlist_id):
        args = PlaylistResource.parser.parse_args()

        playlist = Playlist.query.get(playlist_id)
        if playlist:
            if args['name']:
                playlist.name = args['name']

            db.session.commit()

            return jsonify(playlist.to_dict())
        else:
            return {'message': 'Playlist not found'}, 404

    @login_required
    def delete(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return {'message': 'Playlist deleted'}
        else:
            return {'message': 'Playlist not found'}, 404

class PlaylistSongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('playlist_id', type=int, required=True)
    parser.add_argument('song_id', type=int, required=True)

    @login_required
    def post(self):
        args = PlaylistSongResource.parser.parse_args()

        # Check if playlist and song exist
        playlist = Playlist.query.get(args['playlist_id'])
        song = Song.query.get(args['song_id'])

        if playlist and song:
            # Add song to playlist
            playlist_song = PlaylistSong(playlist_id=args['playlist_id'], song_id=args['song_id'])
            db.session.add(playlist_song)
            db.session.commit()

            return jsonify(playlist_song.to_dict()), 201
        else:
            return {'message': 'Playlist or song not found'}, 404

    @login_required
    def get(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if playlist:
            # Get songs in playlist
            songs = playlist.songs
            return jsonify([song.to_dict() for song in songs])
        else:
            return {'message': 'Playlist not found'}, 404

    @login_required
    def delete(self, playlist_id, song_id):
        playlist = Playlist.query.get(playlist_id)
        song = Song.query.get(song_id)

        if playlist and song:
            # Remove song from playlist
            playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
            if playlist_song:
                db.session.delete(playlist_song)
                db.session.commit()
                return {'message': 'Song removed from playlist'}
            else:
                return {'message': 'Song not found in playlist'}, 404
        else:
            return {'message': 'Playlist or song not found'}, 404

class SongRatingResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=True)
    parser.add_argument('rating', type=int, required=True)

    @login_required
    def post(self):
        args = SongRatingResource.parser.parse_args()

        # Check if song exists
        song = Song.query.get(args['song_id'])

        if song:
            # Create or update rating
            rating = SongRating.query.filter_by(song_id=args['song_id'], user_id=current_user.id).first()
            if rating:
                rating.rating = args['rating']
            else:
                rating = SongRating(song_id=args['song_id'], user_id=current_user.id, rating=args['rating'])
                db.session.add(rating)

            db.session.commit()

            return jsonify(rating.to_dict()), 201
        else:
            return {'message': 'Song not found'}, 404

    @login_required
    def get(self, rating_id):
        rating = SongRating.query.get(rating_id)
        if rating:
            return jsonify(rating.to_dict())
        else:
            return {'message': 'Rating not found'}, 404

    @login_required
    def put(self, rating_id):
        args = SongRatingResource.parser.parse_args()

        rating = SongRating.query.get(rating_id)
        if rating:
            rating.rating = args['rating']
            db.session.commit()
            return jsonify(rating.to_dict())
        else:
            return {'message': 'Rating not found'}, 404

    @login_required
    def delete(self, rating_id):
        rating = SongRating.query.get(rating_id)
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return {'message': 'Rating deleted'}
        else:
            return {'message': 'Rating not found'}, 404

class AlbumRatingResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('album_id', type=int, required=True)
    parser.add_argument('rating', type=int, required=True)

    @login_required
    def post(self):
        args = AlbumRatingResource.parser.parse_args()

        # Check if album exists
        album = Album.query.get(args['album_id'])

        if album:
            # Create or update rating
            rating = AlbumRating.query.filter_by(album_id=args['album_id'], user_id=current_user.id).first()
            if rating:
                rating.rating = args['rating']
            else:
                rating = AlbumRating(album_id=args['album_id'], user_id=current_user.id, rating=args['rating'])
                db.session.add(rating)

            db.session.commit()

            return jsonify(rating.to_dict()), 201
        else:
            return {'message': 'Album not found'}, 404

    @login_required
    def get(self, rating_id):
        rating = AlbumRating.query.get(rating_id)
        if rating:
            return jsonify(rating.to_dict())
        else:
            return {'message': 'Rating not found'}, 404

    @login_required
    def put(self, rating_id):
        args = AlbumRatingResource.parser.parse_args()

        rating = AlbumRating.query.get(rating_id)
        if rating:
            rating.rating = args['rating']
            db.session.commit()
            return jsonify(rating.to_dict())
        else:
            return {'message': 'Rating not found'}, 404

    @login_required
    def delete(self, rating_id):
        rating = AlbumRating.query.get(rating_id)
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return {'message': 'Rating deleted'}
        else:
            return {'message': 'Rating not found'}, 404

class SongFlagResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=True)

    @login_required
    def post(self):
        args = SongFlagResource.parser.parse_args()

        # Check if song exists
        song = Song.query.get(args['song_id'])

        if song:
            # Create or update flag
            flag = SongFlag.query.filter_by(song_id=args['song_id'], user_id=current_user.id).first()
            if flag:
                # You might want to handle logic for toggling the flag here
                return {'message': 'Flag already exists'}, 400
            else:
                flag = SongFlag(song_id=args['song_id'], user_id=current_user.id)
                db.session.add(flag)

            db.session.commit()

            return jsonify(flag.to_dict()), 201
        else:
            return {'message': 'Song not found'}, 404

    @login_required
    def get(self, flag_id):
        flag = SongFlag.query.get(flag_id)
        if flag:
            return jsonify(flag.to_dict())
        else:
            return {'message': 'Flag not found'}, 404

    @login_required
    def delete(self, flag_id):
        flag = SongFlag.query.get(flag_id)
        if flag:
            db.session.delete(flag)
            db.session.commit()

            return {'message': 'Flag deleted'}
        else:
            return {'message': 'Flag not found'}, 404

# ... (other flag management endpoints: get, delete, put)
class AlbumSongResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('album_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('song_id', type=int, required=True, help="This field cannot be left blank!")

    @login_required
    def get(self, album_id):
        album_songs = AlbumSong.query.filter_by(album_id=album_id).all()
        if album_songs:
            return jsonify({'song_ids': [album_song.song_id for album_song in album_songs]})
        else:
            return jsonify({'message': 'No songs found for this album'}), 404
         
    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to create album songs
    def post(self):
        data = AlbumSongResource.parser.parse_args()
        album_song = AlbumSong(album_id=data['album_id'], song_id=data['song_id'])
        db.session.add(album_song)
        db.session.commit()
        return jsonify(AlbumSong.to_dict()), 201

    @login_required
    @roles_required('creator', 'admin')  # Allow creators and admins to delete album songs
    def delete(self, album_id, song_id):
        album_song = AlbumSong.query.filter_by(album_id=album_id, song_id=song_id).first()
        if album_song:
            db.session.delete(album_song)
            db.session.commit()
            return jsonify( {'message': 'AlbumSong deleted.'})
        else:
            return jsonify( {'message': 'AlbumSong not found'}), 404

class AlbumFlagResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('album_id', type=int, required=True)

    @login_required
    def post(self):
        args = AlbumFlagResource.parser.parse_args()

        # Check if album exists
        album = Album.query.get(args['album_id'])

        if album:
            # Create or update flag
            flag = AlbumFlag.query.filter_by(album_id=args['album_id'], user_id=current_user.id).first()
            if flag:
                # You might want to handle logic for toggling the flag here
                return {'message': 'Flag already exists'}, 400
            else:
                flag = AlbumFlag(album_id=args['album_id'], user_id=current_user.id)
                db.session.add(flag)

            db.session.commit()

            return jsonify(flag.to_dict()), 201
        else:
            return {'message': 'Album not found'}, 404

    @login_required
    def get(self, flag_id):
        flag = AlbumFlag.query.get(flag_id)
        if flag:
            return jsonify(flag.to_dict())
        else:
            return {'message': 'Flag not found'}, 404

    @login_required
    def delete(self, flag_id):
        flag = AlbumFlag.query.get(flag_id)
        if flag:
            db.session.delete(flag)
            db.session.commit()
            return {'message': 'Flag deleted'}
        else:
            return {'message': 'Flag not found'}, 404

    # ... (other flag management endpoints: put, patch, etc.)

class SearchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str)
        parser.add_argument('artist', type=str)
        parser.add_argument('genre', type=str)
        parser.add_argument('rating', type=int)
        # ... (add more search/filter parameters as needed)
        args = parser.parse_args()

        # Implement search logic based on query parameters
        # Example:
        query = Song.query

        if args['query']:
            query = query.filter(Song.name.like('%' + args['query'] + '%'))
        if args['artist']:
            query = query.filter(Song.artist == args['artist'])
        if args['genre']:
            query = query.filter(Song.genre == args['genre'])
        if args['rating']:
            query = query.filter(Song.rating >= args['rating'])

        # ... (add more search/filter conditions)

        results = query.all()

        return jsonify([song.to_dict() for song in results])

# ... (add resources to API)