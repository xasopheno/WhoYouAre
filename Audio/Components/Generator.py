import numpy as np
import pyaudio
import time
import threading
import random
import tensorflow as tf
import os
import sys
sys.path.append(os.getcwd())

from Audio.Components.MidiPlayer import MidiPlayer
from Audio.Components.StreamToFrequency import StreamToFrequency
from Audio.Components.Store import Store
from Audio.Components.File_Writer import FileWriter
from Audio.Components.WebSocketPlayer import WebSocketPlayer
from Audio.Components.WebSocketAPI import WebSocketAPI

from Audio.Components.helpers.logger import logger
from Audio.Components.helpers.load_model import load_model
from Audio.Components.helpers.midi_to_hertz import midi_to_hertz
from Audio.Components.helpers.prepare_arrays import get_categorized_variables
from Audio.Components.helpers.create_categorical_indicies import create_lookup_indicies
from Audio.Components.helpers.make_encoded_prediction import make_encoded_prediction
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.play_generated_phrase import play_generated_phrase
from Helpers.map_midi_to_interval import map_midi_to_interval
from Helpers.map_midi_to_note_number import map_midi_to_note_number
import constants

from Audio.Player.osc import SineOsc


class Generator:
    def __init__(self, args=None):
        self.arguments = args
        self.write_csv = args.write_csv
        self.play_midi = args.play_midi
        self.show_prediction = args.display_prediction
        self.play_websocket = args.play_websocket
        self.display_volume = args.display_volume
        self.client = args.client
        self.filtered = args.filtered
        self.nn = args.nn
        self.wave = args.wave

        self.writer = FileWriter(write=self.write_csv)
        self.store = Store()
        self.detector = StreamToFrequency(store=self.store,
                                          show_volume=self.display_volume)

        """Players"""
        self.osc = SineOsc()
        self.player = self.setup_midi_player()
        self.websocket_player = self.setup_websocket_player()

        """Client"""
        if args.client:
            self.api = WebSocketAPI()
            self.api.connect_to_socket()

        """Trained_Model"""
        if args.nn:
            self.counter = 0
            self.prediction_lock = threading.Lock()
            self.n_time_steps = constants.n_time_steps

            self.categorized_variables = get_categorized_variables()

            self.lookup_indicies = create_lookup_indicies(self.categorized_variables)

            self.model = load_model(args.model[0])
            self.graph = tf.get_default_graph()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=constants.sample_rate,
                                  frames_per_buffer=constants.chunk_size,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

        thread = threading.Thread(target=self.generate_and_play_prediction)
        thread.daemon = True
        thread.start()

    def setup_websocket_player(self):
        wsp = WebSocketPlayer()
        if self.play_websocket:
            wsp.connect_to_socket()
        return wsp

    def setup_midi_player(self):
        player = None
        if self.play_midi or self.nn:
            try:
                player = MidiPlayer()
                logger('Connected to Midi Player')
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

    def generate_prediction_phrases(self,
                                    model,
                                    phrases,
                                    categorized_variables,
                                    lookup_indicies,
                                    n_time_steps,
                                    diversity,
                                    n_to_generate):
        pass

    def generate_predictions(self, temperature=1.0):
        n_to_generate = random.choice([10,11,12,13,14,15])
        print('n_to_generate', n_to_generate)

        generated_notes = []
        generated_lengths = []
        phrases = {'note_phrase': list(self.store.note_ring_buffer),
                   'length_phrase': list(self.store.length_ring_buffer)}

        phrases['interval_phrase'] = map_midi_to_interval(phrases['note_phrase'], 0)
        phrases['note_name_phrase'] = map_midi_to_note_number(phrases['note_phrase'])

        start = time.time()
        for step in range(n_to_generate):
            encoded_prediction = make_encoded_prediction(
                model=self.model,
                phrases=phrases,
                categorized_variables=self.categorized_variables,
                lookup_indicies=self.lookup_indicies,
                n_time_steps=self.n_time_steps
            )

            predictions = decode_predictions(
                temperature=temperature,
                encoded_prediction=encoded_prediction,
                lookup_indicies=self.lookup_indicies,
            )

            generated_notes.append(predictions['note_prediction'])
            generated_lengths.append(predictions['length_prediction'])

            last = generated_notes[0]
            phrases['note_phrase'] = np.append(phrases['note_phrase'][1:],
                                               predictions['note_prediction'])
            phrases['length_phrase'] = np.append(phrases['length_phrase'][1:],
                                                 predictions['length_prediction'])

            phrases['interval_phrase'] = map_midi_to_interval(phrases['note_phrase'], last)
            phrases['note_name_phrase'] = map_midi_to_note_number(phrases['note_phrase'])


        end = time.time()
        print('time:', end - start)
        return generated_notes, generated_lengths

    def generate_and_play_prediction(self):
        with self.graph.as_default():
            while True:
                if self.counter > 0:
                    generated_notes, generated_lengths = \
                        self.generate_predictions(temperature=0.5)

                    play_generated_phrase(
                        generated_notes=generated_notes,
                        generated_lengths=generated_lengths,
                        player=self.player,
                        client=self.api,
                    )

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
                    self.counter += 1
                    print('_____________________', self.store.note_ring_buffer)
                    # print('_____________________', self.store.length_ring_buffer)

                if self.client:
                    self.api.model_input({
                        "note": list(self.store.note_ring_buffer),
                        "length": list(self.store.length_ring_buffer),
                    })

        self.store.past_prediction = self.store.values
