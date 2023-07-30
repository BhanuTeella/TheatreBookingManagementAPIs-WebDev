# Import the necessary modules for working with databases and Flask
# `declarative_base` is used to define declarative base classes for models
# `SQLAlchemy` is used to interact with the database
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

# Create a global SQLAlchemy instance
# This instance will be used to interact with the database in our Flask application
db = SQLAlchemy()

# Define a global declarative base class for models
# This base class will be used to define our models as subclasses
Base = declarative_base()

