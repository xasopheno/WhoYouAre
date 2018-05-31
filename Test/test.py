from typing import List
import random

maj = [2, 2, 1, 2, 2, 2, 1]


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


def generate_test_data_array(midi_key: List[int], n_to_generate: int, size: int = 30) -> List[List[int]]:
    return [generate_test_datum(midi_key, size) for _ in range(n_to_generate)]


if __name__ == "__main__":
    result = generate_test_data_array(
        midi_key=generate_key(60, maj, 2),
        n_to_generate=20
    )
