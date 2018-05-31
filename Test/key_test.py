from typing import List
import random
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Audio.Components.helpers.make_encoded_prediction import make_encoded_prediction
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.create_categorical_indicies import create_category_indicies
from Audio.Components.helpers.prepare_arrays import prepare_notes, prepare_lengths
from Audio.Components.helpers.load_model import load_model

major = [2, 2, 1, 2, 2, 2, 1]

notes = prepare_notes()
lengths = prepare_lengths()

note_index, index_note = \
    create_category_indicies(category=notes)
length_index, index_length = \
    create_category_indicies(category=lengths)

lookup_indicies = {
    'note_index': note_index,
    'index_note': index_note,
    'lengths_index': length_index,
    'index_lengths': index_length,
}

categorized_variables = {
    'note_categories': notes,
    'length_categories': lengths
}

model = load_model('45000')


def generate_key(root: int, scale: List[int], n_octaves: int) -> List[int]:
    current = root
    midi_key = [60]

    for octave in range(n_octaves):
        for value in scale:
            current += value
            midi_key.append(current)

    print(midi_key)
    return midi_key


def generate_test_datum(midi_key: List[int], size: int) -> List[int]:
    def choose_random_element():
        rand = random.randrange(0, len(midi_key) -1)
        return midi_key[rand]

    datum = [choose_random_element() for _ in range(size)]
    print(datum)
    return datum


def generate_test_data_array(scope: List[int], n_to_generate: int, size: int = 30) -> List[List[int]]:
    return [generate_test_datum(scope, size) for _ in range(n_to_generate)]


test_key = generate_key(48, major, 3)

note_phrases = generate_test_data_array(
    scope=test_key,
    n_to_generate=20
)

length_phrases = generate_test_data_array(
    scope=lengths,
    n_to_generate=20
)


for phrase in range(len(note_phrases)):
    phrases = {'note_phrase': note_phrases[phrase],
               'length_phrase': length_phrases[phrase]}

    encoded_prediction = make_encoded_prediction(
        model=model,
        phrases=phrases,
        categorized_variables=categorized_variables,
        lookup_indicies=lookup_indicies,
        n_time_steps=30
    )

    predictions = decode_predictions(
        temperature=1,
        encoded_prediction=encoded_prediction,
        lookup_indicies=lookup_indicies,
    )

    note_prediction = predictions['note_prediction']
    print('prediction', phrase, note_prediction)

    result = 0
    if (note_prediction in test_key or note_prediction == 0):
        result += 1
print({})
