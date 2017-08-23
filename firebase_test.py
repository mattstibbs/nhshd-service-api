from firebase import firebase


firebase = firebase.FirebaseApplication('https://nhs-ugo.firebaseio.com/', None)

service_id = "RW3RE"
feedback = 4


count = 0
    # @app.route(‘/api/put’, methods=[‘GET’, ‘POST’])
def fireput():

    global count
    count += 1
    insert_data = {'Rating' : feedback, 'Service' : service_id}
    firebase.put('/feedback', 'report' + str(count), insert_data)

fireput()

service_id = "TEST"
feedback = 10

fireput()

print(count)