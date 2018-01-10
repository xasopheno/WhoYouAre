import math


class Store:
    def __init__(self):
        self.__note = 0
        self.__volume = 0
        self.length = 1

        self.volume_array = []

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

    def inc_length(self):
        self.length += 1

    @staticmethod
    def scale_volume(volume):
        volume = round(volume, 6) * 10 ** 3
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
