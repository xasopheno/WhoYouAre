import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.WebSocketPlayer import WebSocketPlayer
from Audio.Components.helpers.midi_to_hertz import midi_to_hertz
from Audio.Player.osc import SineOsc
from Audio.Components.helpers.logger import logger_error


class CSVPlayer:
    def __init__(self, args=None):
        self.file_path = self.get_file_path(args.filename[0])
        self.play_ws = args.play_ws
        self.play_pyosc = args.play_pyosc


        # self.ws_player = WebSocketPlayer()
        # self.ws_player.connect_to_socket()

        self.pyosc_player = SineOsc()

    @staticmethod
    def get_file_path(filename):
        if not filename:
            logger_error('CSV player requires a filename')

        else:
            current_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data', filename))
            print(current_path)
            return current_path

    def play_csv(self):
        with open(self.file_path, 'r') as f:
            next(f)
            for line in f:
                print(line)
                # print(line)
                line = line.split(',')
                midi = line[0]
                length = line[1]
                volume = line[2]
                if self.play_ws:
                    self.ws_player.play(int(midi))
                if self.play_pyosc:
                    self.pyosc_player.freq = midi_to_hertz(int(midi))
                time.sleep(float(length))
            self.pyosc_player.freq = 0
            time.sleep(.5)
