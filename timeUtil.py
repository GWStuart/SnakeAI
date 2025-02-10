"""
File to help handle time recordings in the program
"""
import time

"""
Class acting as a simple timer with custom display output
"""
class Timer:
    def __init__(self):
        self.t1 = None  # start time
        self.t2 = None  # end time

    """
    Start the timer
    """
    def start(self):
        self.t1 = time.time()

    """
    Stop the timer
    """
    def stop(self):
        self.t2 = time.time()

    """
    Return a formatted string representing elapsed time
    @param seconds_accuracy the number of decimal places with which to display the seconds
    """
    def get_elapsed_time(self, SECONDS_ACCURACY=3):
        seconds = self.t2 - self.t1
        return Timer.convert_time(seconds, SECONDS_ACCURACY)

    """
    Convert a time in seconds into a formatted string
    @param seconds_accuracy the number of decimal places with which to display the seconds
    """
    @staticmethod
    def convert_time(seconds: int, SECONDS_ACCURACY=3) -> str:
        if seconds < 60:
            return f"{round(seconds, SECONDS_ACCURACY)}s"

        minutes = int(seconds // 60)
        seconds %= 60
        if minutes < 60:
            return f"{minutes}m {round(seconds, SECONDS_ACCURACY)}s"

        hours = int(minutes // 60)
        minutes %= 60
        seconds %= 60
        return f"{hours}h {minutes}m {round(seconds, SECONDS_ACCURACY)}s"

