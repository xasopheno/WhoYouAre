import numpy as np


def prepare_notes():
    notes = []
    for i in range(0, 128):
        notes.append(i)
    return notes


def prepare_note_names():
    notes_names = []
    for i in range(0, 13):
        notes_names.append(i)
    return notes_names


def prepare_intervals():
    intervals = []
    for i in range(-24, 25):
        intervals.append(i)
    return intervals


def prepare_lengths():
    lengths = []
    first_field = np.arange(0.0, 1., 0.01)
    for value in list(first_field):
        lengths.append(round(value, 2))

    second_field = np.arange(1.0, 5.1, 0.1)
    for value in list(second_field):
        lengths.append(round(value, 1))

    return lengths


def get_categorized_variables():
    return {
        'note_categories': prepare_notes(),
        'length_categories': prepare_lengths(),
        'note_name_categories': prepare_note_names(),
        'interval_categories': prepare_intervals(),
    }