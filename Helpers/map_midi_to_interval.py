from typing import List
import os, sys
sys.path.append(os.getcwd())


def map_midi_to_interval(series_midi_numbers: List[int], last: int) -> List[int]:
    intervals = []
    for index, value in enumerate(series_midi_numbers):
        if index == 0:
            interval = series_midi_numbers[index] - last
        else:
            interval = series_midi_numbers[index] - series_midi_numbers[index - 1]

        while abs(interval) > 24:
            interval = interval / 2

        if series_midi_numbers[index] is not 0 and last is not 0:
            intervals.append(int(interval))
        else:
            intervals.append(0)

    return intervals
