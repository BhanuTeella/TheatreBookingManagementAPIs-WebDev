import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('db_directory/music_streaming_app.db')
c = conn.cursor()

# Insert data into the table
for i in range(1,11):


    c.execute('''
        INSERT INTO Users VALUES (?,?,?,?,?)
    ''', (i, 'user'+str(i), 'user'+str(i)+"@mail.com",'password'+str(i),'user'))
    i=i+1

# Commit the changes and close the connection
conn.commit()
conn.close()