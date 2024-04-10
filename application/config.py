import os

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Define a base configuration class with default settings
class Config(object):
    DEBUG = True
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY='your-secret-key'
    SECURITY_PASSWORD_SALT='your-password-salt'
    SECURITY_REGISTERABLE=True
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_POST_LOGIN_VIEW= 'index'

# Define a production configuration class that inherits from the base class
# This class sets the database directory and URI for a production environment
class ProductionConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(SQLITE_DB_DIR, 'music_streaming_app.db')

# Define a local development configuration class that inherits from the base class
# This class sets the database directory and URI for a local development environment
# It also enables SQLALCHEMY_TRACK_MODIFICATIONS for debugging purposes
class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(SQLITE_DB_DIR, 'music_streaming_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True