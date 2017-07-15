from flask import Flask, jsonify, render_template
import os
import requests
import untangle
from flask_cors import CORS
import re
import config

app = Flask(__name__)

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


@app.route('/directions/<service_id>/<disposition>')
def show_direction(service_id, disposition):
    print(service_id)
    print(disposition)
    response = get_choices_service(service_id)
    return render_template('main2.html',
                           lon=response['lon'],
                           lat=response['lat'],
                           googke_key=google_key)


@app.route('/map/<service_id>')
def show_map(service_id):
    response = get_choices_service(service_id)
    return render_template('main2.html',
                           lon=response['lon'],
                           lat=response['lat'],
                           google_key=google_key)


@app.route('/service/<service_id>')
def get_service_by_id(service_id):

    print(service_id)

    response = get_choices_service(service_id)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
