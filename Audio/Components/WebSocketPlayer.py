import os, sys
import math
from socketIO_client import SocketIO, LoggingNamespace
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.helpers.logger import logger

class WebSocketPlayer:
    def __init__(self):
        self.socket = None

    @staticmethod
    def midi_to_hertz(midi):
        if midi == 0:
            return 0
        f = 2**((midi-69)/12) * 440
        return f

    def connect_to_socket(self):
        socket = SocketIO('localhost', 9876, LoggingNamespace)
        # socket = SocketIO('phone-synth-server.herokuapp.com', 80, LoggingNamespace)
        self.socket = socket

        logger('Connected to localhost:9876')

    def play(self, midi):
        freq = self.midi_to_hertz(midi)
        if freq < 1500:
            self.socket.emit('freq_change', {'freq': freq})
