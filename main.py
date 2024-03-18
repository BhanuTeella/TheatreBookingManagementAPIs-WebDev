import os  
from flask import Flask, render_template 
from flask_restful import Api
from application.database import db  

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
    return app, api  
app, api = create_app() 

from application.controllers import * 
from application.api import * 
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SongResource, '/songs', '/songs/<int:song_id>')
api.add_resource(AlbumResource, '/albums', '/albums/<int:album_id>')
api.add_resource(AlbumSongResource, '/album_songs', '/album_songs/<int:album_id>/<int:song_id>')
api.add_resource(PlaylistResource, '/playlists', '/playlists/<int:playlist_id>')
api.add_resource(PlaylistSongResource, '/playlist_songs', '/playlist_songs/<int:playlist_id>/<int:song_id>')
api.add_resource(RatingResource, '/ratings', '/ratings/<int:rating_id>')
#api.add_resource(FlagResource, '/flags', '/flags/<int:flag_id>')
api.add_resource(SongsByGenreResource, '/songs/genre/<string:genre>')
if __name__ == '__main__': 
    app.run()  