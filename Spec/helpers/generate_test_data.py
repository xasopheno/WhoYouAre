from typing import List
import random

major = [2, 2, 1, 2, 2, 2, 1]


def generate_test_datum(midi_key: List[int], size: int) -> List[int]:
    def choose_random_element():
        rand = random.randrange(0, len(midi_key) -1)
        return midi_key[rand]

    datum = [choose_random_element() for _ in range(size)]
    print(datum)
    return datum


def generate_test_data_array(
        scope: List[int],
        n_to_generate: int,
        size: int = 30
) -> List[List[int]]:
    return [generate_test_datum(scope, size) for _ in range(n_to_generate)]
