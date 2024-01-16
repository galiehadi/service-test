from distutils.log import debug
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS, cross_origin
from utils.func import *
import logging as systemlog

log = systemlog.getLogger('werkzeug')
log.setLevel(systemlog.ERROR)
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
debug_mode = False

# ================================== Service Show All Data ================================== #
@app.route('/service/all/data')
def allData():
    data = {
        'message': 'Failed',
        'total': 1,
        'limit': 1,
        'page': 0,
    }
    try:
        data['object'] = get_all_menu()
        data['message'] = 'Success'
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200  
    except Exception as E:
        data['object'] = []
        data['message'] = str(E)
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500  
    
# ================================== Service Count Price ================================== #
@app.route('/service/count/price', methods=['POST'])
def countPrice():
    try:
        payload = dict(request.get_json())
        objects = count_price(payload)

        response_data = {
            "message": "Success" if objects['Status'] == "Success" else "Failed",
            "object": objects
        }

        return jsonify(response_data)

    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON data: {str(e)}"
        response_data = {
            "message": "Failed",
            "error": error_message
        }
        return make_response(jsonify(response_data), 400)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        response_data = {
            "message": "Failed",
            "error": error_message
        }
        return make_response(jsonify(response_data), 500)


if __name__ == '__main__':
    if debug_mode:
        app.run('0.0.0.0', port=8083, debug=True)
    else:
        app.run('0.0.0.0', port=8083, debug=False)
