from flask import Flask, jsonify, request
from get_files import get_file_names, concat_csv_files
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

file_names = get_file_names()


@app.route('/api/v1/files', methods=['GET'])
def get_tasks():
    response = jsonify({'file_names': file_names})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/v1/files', methods=['POST'])
def make_data():
    print(json.loads(request.data))
    concat_csv_files(json.loads(request.data))
    return jsonify('working')

if __name__ == '__main__':
    app.run(debug=True)
