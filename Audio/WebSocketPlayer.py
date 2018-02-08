import os, sys
from socketIO_client import SocketIO, LoggingNamespace
from Audio.logger import logger
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


class WebSocketPlayer:
    def __init__(self):
        self.socket = None

    @staticmethod
    def midi_to_hertz(midi):
        if midi == 0:
            return 0
        g = 2**(1/12)
        return 440*g**(midi-69)

    def connect_to_socket(self):
        socket = SocketIO('localhost', 9876, LoggingNamespace)
        self.socket = socket

        logger('Connected to localhost:9876')

    def play(self, midi):
        freq = self.midi_to_hertz(midi)
        if freq < 1500:
            self.socket.emit('freq_change', {'freq': freq})
