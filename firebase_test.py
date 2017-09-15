from firebase import firebase
import config

# TODO Add user authentication to Firebase account
database = firebase.FirebaseApplication(config.firebase, None)

service_id = "RW3RE"
feedback = 4


count = 0


def fireput():

    global count
    count += 1
    insert_data = {'Rating': feedback, 'Service': service_id}
    database.put('/feedback', 'report' + str(count), insert_data)

fireput()

print(count)
