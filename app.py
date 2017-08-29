from flask import Flask, jsonify, render_template, request
import os
import requests
import untangle
from flask_cors import CORS
import re
import default_config as config
import text_protocol as protocol
from firebase import firebase
import database as database

app = Flask(__name__)

# This branch contains the firebase link, which is responsible for pushing data to the JSON Firebase backend

# Allow Cross Origin Resource Sharing for routes under the API path so that other services can use the API
regEx = re.compile("/*")
CORS(app, resources={regEx: {"origins": "*"}})

api_key = config.api_key
google_key = config.google_maps_api_key
count = 0
firebase = firebase.FirebaseApplication('https://nhs-ugo.firebaseio.com/', None)


# Define function to scrape the NHS Choices website for the data to display on the relevant service.

def get_choices_service(service_id):

    url = 'http://v1.syndication.nhschoices.nhs.uk/organisations/hospitals/' \
          f'odscode/{service_id}.xml?apikey={api_key}'

    print(url)
    print("Querying Choices DoS")
    r = requests.get(url)

    print("Getting Choices DoS Overview")
    document = untangle.parse(r.text)

    url2 = document.Organisation.ProfileLinks.d2p1_Link[0].d2p1_Uri.cdata
    url2 = url2.replace("overview", "overview.xml")

    r2 = requests.get(url2)

    document2 = untangle.parse(r2.text)

    overview = document2.feed.entry.content.s_overview
    name = overview.s_name.cdata
    ods_code = overview.s_odsCode.cdata
    lat = overview.s_geographicCoordinates.s_latitude.cdata
    lon = overview.s_geographicCoordinates.s_longitude.cdata
    address = overview.s_address
    telephone = overview.s_contact.s_telephone.cdata
    website = overview.s_website.cdata

    data = {
        'name': name,
        'id': ods_code,
        'lat': lat,
        'lon': lon,
        'telephone': telephone,
        'address': {
            'postcode': address.s_postcode.cdata,
        },
        'website': website
        
    }

    return data


@app.route('/map/<service_id>')
# Map page which returns a map to the relevant service. This link will be sent in Text 1.
def show_map(service_id):
    response = get_choices_service(service_id)
    
    return render_template('main2.html',
                           lon=response['lon'],
                           lat=response['lat'],
                           tel=response['telephone'],
                           google_key=google_key)


@app.route('/service/<service_id>')
# Returns the JSON response for a call to the meta function above.
def get_service_by_id(service_id):

    # Make a call to the NHS Choices API to retrieve the information for the specified service ID
    response = get_choices_service(service_id)

    return jsonify(response)


@app.route('/pages/display')
# Return the 'display' page. This is a page which demonstrates the data responses that could be possible.
def display_page():
    return render_template('display.html')


@app.route('/pages/text1')
# Return an HTML example of the SMS that could be sent first
def display_text1():
    return render_template('text1.html')


@app.route('/pages/text2')
# Return an HTML example of the SMS that could be sent second
def display_text2():
    return render_template('text2.html')


@app.route('/pages/thankyou')
# Return an example of the 'response received' page
def display_thankyou():
    return render_template('thankyou.html')


@app.route('/pages/onlinereg')
# Return a page which directs users how to register for NHS online services
def display_onlinereg():
    return render_template('onlinereg.html')


@app.route('/feedback/<service_id>')
# The central feedback page that would be linked to in the second SMS
def show_feedback(service_id):
    response = get_choices_service(service_id)
    return render_template('ratings.html',
                           name=response['name'])


@app.route('/')
# Initial demonstration page which will step through the process
def display_links():
    return render_template('links.html')


@app.route('/post', methods=['POST'])
# First pass at posting to a back end. This method became useless when the back end was altered.
def post_feedback():
    data = request.json
    r = requests.post('http://ec2-13-58-211-169.us-east-2.compute.amazonaws.com/api/feedback',
                      json=data)
    # TODO Test running through MySQL rather than json - See MySQL Branch
    print(r.status_code)
    print(r.text)
    return 'OK', 200


@app.route('/demo', methods=['POST'])
# The main demonstration of the system.  This page will allow a user to fully demonstrate the system working.
def demo():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        service_id = request.form['service_id']
        service_name = request.form['service_name']
        wait_time = request.form['wait_time']
        protocol.send_messages(name, phone_number, service_id, service_name, wait_time)
        return render_template('thankyou.html')
    else:
        return render_template('demo.html')


@app.route('/demonstration', methods=['GET', 'POST'])
# Render the demonstration form in HTML
def demonstration():
    return render_template('demo.html')


@app.route('/mysql', methods=['POST'])
# Method that is now obsolete given the lack of a MySQL back end
def mysql():

    output = request.get_json(force=True)
    print(output)

    service = request.json['dm']
    print(service)

    feedback = request.json['stars']
    print(feedback)

    # TODO Check SQLite port and ensure that port blocking is not the problem
    # https://stackoverflow.com/questions/45567007/sqlite-and-flask-insert-statement-error
    # Method runs as expected from `database.py` but no database insert is made from here
    return 'OK', 200


@app.route('/postjson', methods=['POST'])
# PostMan API testing method. This allows easy testing to ensure that the correct response is returned by the API
def post_json_handler():
    content = request.get_json()
    print(content)
    return 'JSON posted'


@app.route('/database')
# A now obsolete method for posting to a database. See `database.py` for implementation.
def db_insert():
    database.db()
    print('TEST')
    return render_template('display.html')


@app.route('/firebase', methods=['GET', 'POST'])
# The final backend connection for the app. This method takes JSON from the client side JS and posts it to the Firebase
def fireput():

    output = request.get_json(force=True)
    print(output)
    service_id = request.json['dm']
    feedback = request.json['stars']
    global count
    count += 1
    insert_data = {'Rating' : feedback, 'Service' : service_id}
    firebase.put('/feedback', 'report' + str(count), insert_data)
    print('TEST' + str(count))
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
    # TODO Change this to the appropriate webserver IP

