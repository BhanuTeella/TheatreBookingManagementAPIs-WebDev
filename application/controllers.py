from flask import Flask, request, render_template
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from application.models import User 

@app.route('/')
def test_models():
    users = User.query.all()

    return render_template('test_models.html', users=users)