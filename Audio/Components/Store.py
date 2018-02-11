import os
import sys
import math
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.helpers.Timer import Timer


class Store:
    def __init__(self):
        self.__note = 0
        self.__volume = 0
        self.length = 0
        self.past_prediction = self.base_values()
        self.new_note = True
        self.volume_array = []
        self.timer = Timer()


    @staticmethod
    def base_values():
        return {
            "note": 0,
            "volume": 0,
            "length": 0,
        }

    @property
    def note(self):
        return self.__note

    @property
    def volume(self):
        return self.__volume

    @note.setter
    def note(self, note):
        note = int(note)
        self.__note = note
        self.is_new_note()

    @volume.setter
    def volume(self, volume):
        volume = self.scale_volume(volume)
        volume = int(volume)
        self.volume_array.append(volume)
        self.__volume = volume

    @property
    def values(self):
        return {
            "note": self.note,
            "volume": self.avg_volume(),
            "length": self.length,
        }

    @staticmethod
    def scale_volume(volume):
        volume = round(volume, 6) * 10 ** 3
        if volume == 0:
            volume = 0.001
        volume = math.log(volume)
        volume *= 15
        if volume > 127:
            volume = 127
        if volume < 0:
            volume = 0

        return volume

    def reset(self):
        self.length = 1
        self.volume_array = []

    def avg_volume(self):
        length = len(self.volume_array)
        total = sum(self.volume_array)
        avg = total/length if length else 0
        return int(avg)

    def is_new_note(self):
        if self.note == self.past_prediction['note']:
            self.new_note = False
            self.past_prediction = self.values
        else:
            self.new_note = True
            self.past_prediction = self.values
            self.past_prediction['length'] = self.timer.result
            self.timer.start_timer()
            self.reset()

