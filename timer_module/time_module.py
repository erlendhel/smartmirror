import time


class Timer(object):
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_time_in_seconds(self):
        end = time.time()
        s = end - self.start
        time_str = s
        return time_str