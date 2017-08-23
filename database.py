import sqlite3


# TODO Check SQLite port and ensure that port blocking is not the problem
# https://stackoverflow.com/questions/45567007/sqlite-and-flask-insert-statement-error
# Method runs as expected from `database.py` but no database insert is made from here


def db(service, feedback):

    try:
        database = 'UGO.db'
        conn = sqlite3.connect(database)
        c = conn.cursor()
        query = "INSERT INTO ratings (service_id, rating)  VALUES (?, ?)"
        c.execute(query, (service, feedback))
        conn.commit()
        conn.close()
        print('Added to DB')
    except:
        print("An error occurred")

db('TEST', 10)



