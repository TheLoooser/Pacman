""" Based on https://realpython.com/python-timer/ """
import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def pause(self):
        self._elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

    def resume(self):
        self._start_time = time.perf_counter() if not self._start_time else self._start_time

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None and self._elapsed_time == 0:
            raise TimerError(f"Timer is and was not running. Use .start() to start it")

        elapsed_time = self.get_elapsed_time()
        self._start_time = None
        self._elapsed_time = 0
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

    def get_elapsed_time(self):
        return time.perf_counter() - self._start_time + self._elapsed_time if self._start_time else self._elapsed_time


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    time.sleep(2)
    print(timer.get_elapsed_time())
    timer.pause()
    timer.resume()
    time.sleep(1)
    timer.stop()

    timer.start()
    time.sleep(3)
    timer.resume()
    timer.pause()
    timer.stop()


