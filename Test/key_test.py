from collections import Counter
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Audio.Components.helpers.make_encoded_prediction import make_encoded_prediction
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.create_categorical_indicies import create_category_indicies
from Audio.Components.helpers.prepare_arrays import prepare_notes, prepare_lengths
from Audio.Components.helpers.load_model import load_model

from Test.helpers.generate_key import generate_key
from Test.helpers.generate_test_data import generate_test_data_array
from Test.helpers.midi_to_key import midi_to_key

major = [2, 2, 1, 2, 2, 2, 1]
n_tests = 1000
root = 54

notes = prepare_notes()
lengths = prepare_lengths()

note_index, index_note = \
    create_category_indicies(category=notes)
length_index, index_length = \
    create_category_indicies(category=lengths)

lookup_indicies = {
    'note_index': note_index,
    'index_note': index_note,
    'length_index': length_index,
    'index_length': index_length,
}

categorized_variables = {
    'note_categories': notes,
    'length_categories': lengths
}

model = load_model('45000')


test_key = generate_key(48, major, 3)

note_phrases = generate_test_data_array(
    scope=test_key,
    n_to_generate=n_tests
)

length_phrases = generate_test_data_array(
    scope=lengths,
    n_to_generate=n_tests
)

result = 0
total = 0
passing_results = []
failing_results = []

test_key = generate_key(root-12, major, 5)

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
        temperature=0.5,
        encoded_prediction=encoded_prediction,
        lookup_indicies=lookup_indicies,
    )

    note_prediction = predictions['note_prediction']

    if note_prediction is not 0:
        total += 1
        if note_prediction in test_key:
            print('prediction', phrase, note_prediction, 'PASS')
            passing_results.append(midi_to_key[note_prediction])
            result += 1
        else:
            print('prediction', phrase, note_prediction, '**********FAIL')
            failing_results.append(midi_to_key[note_prediction])
    else:
        print('   Predicted 0')

for value in generate_key(root, major, 1):
    print(midi_to_key[value])

print('************RESULT***************')
print('ROOT is ', midi_to_key[root])
print(result, '/', total, 'tests passed')
print('% tests predicted the correct key', result/total)
zeros = n_tests - total
print(zeros, 'tests predicted silence (0)')
print('% tests predicted silence', zeros/n_tests)
print('***passing_results***', Counter(passing_results))
print('!!!failing_results!!!', Counter(failing_results))
