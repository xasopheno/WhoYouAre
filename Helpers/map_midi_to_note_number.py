from typing import List
import os, sys
sys.path.append(os.getcwd())
from Helpers.midi_to_note_number import midi_to_note_number


def map_midi_to_note_number(series_midi_numbers: List[int]):
    return list(map(lambda x: midi_to_note_number[x], series_midi_numbers))