import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
with sqlite3.connect('db_directory/music_streaming_app.db') as conn:
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute("SELECT user_id, password FROM Users")
    users = cursor.fetchall()

    for user in users:
        # Hash the user's password
        hashed_password = generate_password_hash(user[1])
        
        # Update the user's password
        cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (hashed_password, user[0]))

    # Changes are automatically committed and the connection is closed when exiting the 'with' block