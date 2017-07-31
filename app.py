from flask import Flask, jsonify, render_template, request
import os
import requests
import untangle
from flask_cors import CORS
import re
import default_config as config
import text_protocol as protocol

app = Flask(__name__)

#TODO Experiment with MySQL database backend. 

# Allow Cross Origin Resource Sharing for routes under the API path so that other services can use the API
regEx = re.compile("/*")
CORS(app, resources={regEx: {"origins": "*"}})

api_key = config.api_key
google_key = config.google_maps_api_key


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
def show_map(service_id):
    response = get_choices_service(service_id)
    
    return render_template('main2.html',
                           lon=response['lon'],
                           lat=response['lat'],
                           google_key=google_key)


@app.route('/service/<service_id>')
def get_service_by_id(service_id):

    # Make a call to the NHS Choices API to retrieve the information for the specified service ID
    response = get_choices_service(service_id)

    return jsonify(response)


@app.route('/pages/display')
def display_page():
    return render_template('display.html')


@app.route('/pages/text1')
def display_text1():
    return render_template('text1.html')


@app.route('/pages/text2')
def display_text2():
    return render_template('text2.html')


@app.route('/pages/thankyou')
def display_thankyou():
    return render_template('thankyou.html')


@app.route('/pages/onlinereg')
def display_onlinereg():
    return render_template('onlinereg.html')


@app.route('/feedback/<service_id>')
def show_feedback(service_id):
    response = get_choices_service(service_id)
    return render_template('ratings.html',
                           name=response['name'])

@app.route('/')
def display_links():
    return render_template('links.html')


@app.route('/post', methods=['POST'])
def post_feedback():
    data = request.json
    r = requests.post('http://ec2-13-58-211-169.us-east-2.compute.amazonaws.com/api/feedback',
                      json=data)
    #TODO Test running through MySQL rather than json - See MySQL Branch
    print(r.status_code)
    print(r.text)
    return 'OK', 200


@app.route('/demo', methods=['POST'])
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
def demonstration():

    return render_template('demo.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)

