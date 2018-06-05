from Helpers.midi_to_note_number import midi_to_note_number
from typing import List


def add_intervals_and_note_names(line: List[str], last: int) -> List:
    line_copy = line[:]
    midi_num = (int(line_copy[0]))

    line_copy = add_intervals(line_copy, midi_num)
    line_copy = add_note_names(line_copy, midi_num, last)

    return line_copy


def add_note_names(line: List[str], midi_num: int):
    line_copy = line[:]

    if midi_num == 0:
        line_copy.insert(1, '0')
    else:
        line_copy.insert(1, midi_to_note_number[midi_num])

    return line_copy


def add_intervals(line: List, midi_num: int, last: int):
    line_copy = line[:]

    interval = midi_num - last

    while abs(interval) > 24:
        interval = interval / 2
    if midi_num is not 0 and last is not 0:
        line_copy.insert(2, interval)
    else:
        line_copy.insert(2, '0')

    return line_copy

