import os.path
import sys

sys.path.append(os.getcwd())

from Audio.Components.helpers.prepare_arrays import prepare_lengths, prepare_notes
from Test.helpers.generate_key import generate_key
from Test.helpers.generate_test_data import generate_test_data_array
from Helpers.map_midi_to_note_number import map_midi_to_note_number
from Helpers.map_midi_to_interval import map_midi_to_interval
from Helpers.midi_to_key import midi_to_key


def get_path(filename):
    current_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    path = '{0}/{1}'.format(current_path, filename)

    print('Data will be written to:', path)
    return path


file_name = get_path('generated_key_data.csv')
file = open(file_name, "w")

major = [2, 2, 1, 2, 2, 2, 1]

notes = prepare_notes()
lengths = prepare_lengths()

for root in range(36, 59):
    test_key = generate_key(root, major, 3)

    note_phrases = generate_test_data_array(
        scope=test_key,
        n_to_generate=1,
        size=1000
    )[0]

    length_phrases = generate_test_data_array(
        scope=lengths,
        n_to_generate=1,
        size=1000
    )[0]

    note_names = map_midi_to_note_number(note_phrases)
    intervals = map_midi_to_interval(note_phrases, 0)

    for n in range(len(note_phrases)):
        line = "{}, {}, {}\n".format(
            note_phrases[n],
            # note_names[n],
            # intervals[n],
            length_phrases[n],
            1,
            )
        print(line)

        file.write(line)
    # file.write('****************\n')
