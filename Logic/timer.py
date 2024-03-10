"""
This module implements a timer.
Code is based on: https://realpython.com/python-timer/
"""
import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    """
    A class to represent a timer.
    """
    def __init__(self) -> None:
        """
        Constructs a timer object.
        """
        self._start_time = None
        self._elapsed_time = 0

    def start(self) -> None:
        """
        Starts a new timer.

        :return: Nothing.
        """
        # if self._start_time is not None:
        #     raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def pause(self) -> None:
        """
        Pauses the timer.

        :return: Nothing.
        """
        self._elapsed_time = self._elapsed_time + time.perf_counter() - self._start_time
        self._start_time = None

    def resume(self) -> None:
        """
        Resumes the timer.

        :return: Nothing.
        """
        self._start_time = time.perf_counter() if not self._start_time else self._start_time

    def stop(self) -> None:
        """
        Stop the timer, and report the elapsed time

        :return: Nothing.
        """
        if self._start_time is None and self._elapsed_time == 0:
            raise TimerError("Timer is and was not running. Use .start() to start it")

        # print(f"Elapsed time: {self.get_elapsed_time():0.4f} seconds")
        self._start_time = None
        self._elapsed_time = 0

    def get_elapsed_time(self) -> int:
        """
        Gets the elapsed time.

        :return: The elapsed time.
        """
        return time.perf_counter() - self._start_time + self._elapsed_time if self._start_time else self._elapsed_time

    def is_running(self) -> bool:
        """
        Checks whether the timer is running or not.

        :return: True if the timer is active, False otherwise.
        """
        return self._start_time is not None


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
    print(timer.is_running())
    time.sleep(3)
    timer.resume()
    timer.pause()
    timer.stop()
    print(timer.is_running())
