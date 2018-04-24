import os, sys
from socketIO_client import SocketIO, LoggingNamespace
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.helpers.logger import logger


class WebSocketAPI:
    def __init__(self):
        self.socket = None

    def connect_to_socket(self):
        socket = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.socket = socket

        logger('Connected to http://127.0.0.1:5000')

    def model_input(self, data):
        self.socket.emit('model_input', {'data': data})

    def model_output(self, data):
        self.socket.emit('model_output', {'data': data})
