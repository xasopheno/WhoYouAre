import os, sys

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import socketio
import eventlet
import eventlet.wsgi
sys.path.append(os.getcwd())
print(sys.path)
from Helpers.get_files import get_file_names, concat_csv_files

sio = socketio.Server(logger=True)
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


@sio.on('connect')
def connect(sid, environ):
    print('client_connect', sid)
    sio.emit(
        'connected_to_server',
        {'message': 'Connected'},
    )


@sio.on('model_input')
def model_input(sid, data):
    print(data)
    sio.emit('model_input', data)


@sio.on('model_output')
def model_output(sid, data):
    print(data)
    sio.emit('model_output', data)


if __name__ == '__main__':
    app = socketio.Middleware(sio, app)

    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 2345)), app)
