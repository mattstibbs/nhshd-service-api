import sqlite3


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

# db('TEST', 10)



