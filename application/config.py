import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(SQLITE_DB_DIR, 'theatre_shows_database.db')

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(SQLITE_DB_DIR, 'theatre_shows_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True