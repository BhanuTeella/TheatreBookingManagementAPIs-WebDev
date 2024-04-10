import os
from flask import Flask, render_template
from flask_restful import Api
from application.database import db
from flask_security import Security, SQLAlchemyUserDatastore
from application.models import User, Role

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder='templates')
    if os.getenv('ENV', 'development') == "production":
        raise NotImplementedError("Production environment not implemented")
    else:
        app.config.from_object('application.config.LocalDevelopmentConfig')

    db.init_app(app)
    api = Api(app)
    app.app_context().push()

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    app.logger.info("App created successfully")
    return app, api

app, api = create_app()

from application.controllers import *
from application.api import *

# Add API resources
api.add_resource(LoginResource, '/api/auth/login')
api.add_resource(RegisterResource, '/api/auth/register')
api.add_resource(LogoutResource, '/api/auth/logout')

api.add_resource(UserResource, '/api/users/<int:user_id>')

api.add_resource(SongResource, '/api/songs', '/api/songs/<int:song_id>')
api.add_resource(SongFileResource, '/api/songs/<int:song_id>/file')

api.add_resource(AlbumResource, '/api/albums', '/api/albums/<int:album_id>')

api.add_resource(PlaylistResource, '/api/playlists', '/api/playlists/<int:playlist_id>')
api.add_resource(PlaylistSongResource, '/api/playlists/<int:playlist_id>/songs', '/api/playlists/<int:playlist_id>/songs/<int:song_id>')

api.add_resource(SongRatingResource, '/api/songs/<int:song_id>/rate', '/api/songs/ratings/<int:rating_id>')
api.add_resource(AlbumRatingResource, '/api/albums/<int:album_id>/rate', '/api/albums/ratings/<int:rating_id>')

api.add_resource(SongFlagResource, '/api/songs/<int:song_id>/flag', '/api/songs/flags/<int:flag_id>')
api.add_resource(AlbumFlagResource, '/api/albums/<int:album_id>/flag', '/api/albums/flags/<int:flag_id>')

api.add_resource(AlbumSongResource, '/api/albums/<int:album_id>/songs', '/api/albums/<int:album_id>/songs/<int:song_id>')

api.add_resource(AdminDashboardResource, '/api/admin/dashboard')

api.add_resource(SearchResource, '/api/search')

if __name__ == '__main__':
    app.run()