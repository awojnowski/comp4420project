import time

class Timer:
    def __init__(self):
        self.elapsed_time = 0
        self.start_time = 0
        pass


    def start(self):
        if self.start_time > 0:
            pass
        self.start_time = time.time()


    def end(self):
        if self.elapsed_time > 0:
            pass
        self.elapsed_time = time.time() - self.start_time