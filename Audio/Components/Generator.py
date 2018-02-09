import os.path
import pyaudio
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.MidiPlayer import MidiPlayer
from Audio.Components.StreamToFrequency import StreamToFrequency
from Audio.Components.Store import Store
from Audio.Components.File_Writer import File_Writer
from Audio.Components.WebSocketPlayer import WebSocketPlayer
from Audio.Components.helpers.logger import logger


class Generator:
    def __init__(self, args=None):
        self.arguments = args
        self.write_csv = args.write_csv
        self.play_midi = args.play_midi
        self.show_prediction = args.display_prediction
        self.play_websocket = args.play_websocket
        self.display_volume = args.display_volume
        self.filtered = args.filtered

        self.writer = File_Writer(write=self.write_csv)
        self.store = Store()
        self.detector = StreamToFrequency(store=self.store, show_volume=self.display_volume)

        self.subdivision = 0.01
        self.volume_array = []
        self.counter = 1
        self.past_pred = 0
        self.new_note = False

        self.past_predicted_values = self.base_values()

        """Players"""
        self.player = self.setup_midi_player()
        self.websocket_player = self.setup_websocket_player()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    @staticmethod
    def base_values():
        return {
            "note": 0,
            "volume": 0,
            "length": 0,
        }

    def setup_websocket_player(self):
        wsp = WebSocketPlayer()
        if self.play_websocket:
            wsp.connect_to_socket()
        return wsp

    def setup_midi_player(self, synth='Volca'):
        player = None
        if self.play_midi:
            try:
                player = MidiPlayer(synth=synth)
                logger('Connected to', synth)
            except:
                print('No midi destinations!')
        return player

    def generate(self):
        while True:
            if self.store.note == self.past_pred:
                self.store.inc_length()
                self.new_note = False
                self.past_pred = self.store.note
            else:
                self.new_note = True
                self.past_pred = self.store.note
                self.store.reset()
            self.play()
            time.sleep(.001)

    def beyond_threshold(self):
        threshold = True
        if self.filtered:
            threshold = self.new_note

        return threshold

    def play(self):
        note = self.store.note
        volume = self.store.volume
        length = self.store.length

        if self.beyond_threshold():
            if self.write_csv:
                self.writer.write_to_csv(self.past_predicted_values)

            if self.play_midi:
                self.player.play(note, self.subdivision, volume)

            if self.play_websocket:
                self.websocket_player.play(note)

            if self.show_prediction:
                print(self.past_predicted_values)

        self.past_predicted_values = self.store.values
