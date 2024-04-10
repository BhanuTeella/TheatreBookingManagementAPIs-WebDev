from application.models import User
from application.models import db
from main import app  # Import your Flask application instance
import uuid

# Create an application context
with app.app_context():
    # Fetch all users from the database
    users = User.query.all()

    for user in users:
        # Generate a unique fs_uniquifier
        fs_uniquifier = str(uuid.uuid4())
        # Assign the fs_uniquifier to the user
        user.fs_uniquifier = fs_uniquifier

    # Commit the changes to the database
    db.session.commit()