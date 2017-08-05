import sqlite3


def db():

    database = 'UGO.db'
    conn = sqlite3.connect(database)
    c = conn.cursor()
    query = "INSERT INTO ratings (service_id, rating)  VALUES ('RW3RE', 2)"
    c.execute(query)
    conn.commit()
    print('Added to DB')


db()



