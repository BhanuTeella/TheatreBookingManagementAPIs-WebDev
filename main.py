import os  
from flask import Flask, render_template 
from flask_restful import Api, Resource  
from flask_sqlalchemy import SQLAlchemy  
from application.database import db  

app = None  # Initialize the app variable to None
api = None  # Initialize the api variable to None

def create_app():  # Define a function named create_app
    app = Flask(__name__, template_folder='templates')  # Create a Flask app instance with the name of the current module and a template folder
    if os.getenv('ENV', 'development') == "production":  # Check if the environment variable ENV is set to "production"
        raise NotImplementedError("Production environment not implemented")  # If so, raise a NotImplementedError
    else:
        app.config.from_object('application.config.LocalDevelopmentConfig')  # Otherwise, load the LocalDevelopmentConfig object from the application.config module
    db.init_app(app)  # Initialize the SQLAlchemy database with the Flask app instance
    api = Api(app)  # Create an instance of the Flask-RESTful API with the Flask app instance
    app.app_context().push()  # Push the Flask app context to the top of the context stack
    return app, api  # Return the Flask app instance and the Flask-RESTful API instance

app, api = create_app()  # Call the create_app function and assign the returned Flask app instance and Flask-RESTful API instance to the app and api variables

from application.controllers import *  # Import all modules from the application.controllers package

from application.api import *  # Import all modules from the application.api package
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(TheatreResource, '/theatres', '/theatres/<int:theatre_id>')
api.add_resource(MovieResource, '/movies', '/movies/<int:movie_id>')
api.add_resource(ShowResource, '/shows', '/shows/<int:show_id>')
api.add_resource(BookingResource, '/bookings', '/bookings/<int:booking_id>')


if __name__ == '__main__':  # Check if the current module is being run as the main program
    app.run()  # If so, start the Flask app by calling the run method on the Flask app instance
