import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def start_timer(self):
        self.start = time.time()

    @property
    def result(self):
        end = time.time()
        result = end - self.start
        return result
