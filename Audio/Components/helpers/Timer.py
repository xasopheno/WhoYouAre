import time


class Timer:
    def __init__(self):
        self.start = None

    def start_time(self):
        return self.start

    def start(self):
        self.start = time.time()

    @property
    def result(self):
        end = time.time()
        result = end - self.start
        return result
