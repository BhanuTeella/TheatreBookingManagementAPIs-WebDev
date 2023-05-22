import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from application.database import db

app =None

def create_app():
    app = Flask(__name__, template_folder='templates')
    if os.getenv('ENV', 'development')=="production":
        raise NotImplementedError("Production environment not implemented")
    else:
        app.config.from_object('application.config.LocalDevelopmentConfig')
    db.init_app(app)
    app.app_context().push()
    return app
app = create_app()

from application.controllers import *

if __name__ == '__main__':
    app.run()
    
