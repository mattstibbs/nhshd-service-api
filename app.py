from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/service/<service_id>')
def get_service_by_id(service_id):

    response_object = {
        'name': 'Townsville Urgent Treatment Centre',
        'phone': '0113495837',
        'address': 'Townsville Road, Townsville, Manchester, MT5 3RD'
    }
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()