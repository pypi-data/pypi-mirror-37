import time


class Timer:
    _start = None
    _stop = None

    def start(self):
        self._start = time.time()

    def stop(self):
        self._stop = time.time()

    def duration(self):
        return self._stop - self._start


def timer():
    timer_obj = Timer()
    timer_obj.start()
    return timer_obj
