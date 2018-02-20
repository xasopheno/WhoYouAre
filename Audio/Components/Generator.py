import sys
import os.path
import numpy as np
import pyaudio
import time
from keras.models import model_from_json
from Audio.Components.MidiPlayer import MidiPlayer
from Audio.Components.StreamToFrequency import StreamToFrequency
from Audio.Components.Store import Store
from Audio.Components.File_Writer import File_Writer
from Audio.Components.WebSocketPlayer import WebSocketPlayer
from Audio.Components.helpers.logger import logger
from Audio.Player.osc import SineOsc
from Audio.Components.helpers.midi_to_hertz import midi_to_hertz


class Generator:
    def __init__(self, args=None):
        self.arguments = args
        self.write_csv = args.write_csv
        self.play_midi = args.play_midi
        self.show_prediction = args.display_prediction
        self.play_websocket = args.play_websocket
        self.display_volume = args.display_volume
        self.filtered = args.filtered
        self.nn = args.nn
        self.wave = args.wave

        self.writer = File_Writer(write=self.write_csv)
        self.store = Store()
        self.detector = StreamToFrequency(store=self.store, show_volume=self.display_volume)

        """Players"""
        self.osc = SineOsc()
        self.player = self.setup_midi_player()
        self.websocket_player = self.setup_websocket_player()

        """Trained_Model"""
        if args.nn:
            self.model = self.load_model()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    @staticmethod
    def load_model():
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        return loaded_model

    def setup_websocket_player(self):
        wsp = WebSocketPlayer()
        if self.play_websocket:
            wsp.connect_to_socket()
        return wsp

    def setup_midi_player(self):
        player = None
        if self.play_midi:
            try:
                player = MidiPlayer()
                logger('Connected')
            except:
                print('No midi destinations!')
        return player

    def generate(self):
        while True:
            self.play()
            time.sleep(0.0001)

    def beyond_threshold(self):
        threshold = True
        if self.filtered:
            threshold = self.store.new_note
        return threshold

    @staticmethod
    def most_common(lst):
        return max(set(lst), key=lst.count)

    def make_prediction(self, current_phrase):
        x_pred = np.zeros((1, self.n_time_steps, len(self.notes)))

        for t, event in enumerate(current_phrase):
            x_pred[0, t, self.note_index[event]] = 1.

        note_pred = self.loaded_model.predict(x_pred, verbose=0)[0]

        note_index_from_sample = self.sample(note_pred, 1.0)
        note_prediction = self.index_note[note_index_from_sample]
        self.store.update_neural_path(note_prediction)

        freq_pred = self.midi_to_hertz(note_prediction)
        return freq_pred

    @staticmethod
    def prepare_notes():
        notes = []
        for i in range(0, 128):
            notes.append(i)
        print(notes)
        return notes

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def play(self):
        note = self.store.note
        volume = self.store.volume
        length = self.store.length

        if self.beyond_threshold():
            if self.store.past_prediction['length'] > 0:
                if self.write_csv:
                    self.writer.write_to_csv(self.store.past_prediction)

                if self.play_midi:
                    self.player.play(note, self.store.length, volume)

                if self.play_websocket:
                    self.websocket_player.play(note)

                if self.show_prediction:
                    print(self.store.past_prediction)

                if self.wave:
                    hertz = midi_to_hertz(note)
                    self.osc.freq = hertz
                    # self.osc.freq = note

                if self.nn:
                    self.play_nn()

        self.store.past_prediction = self.store.values
