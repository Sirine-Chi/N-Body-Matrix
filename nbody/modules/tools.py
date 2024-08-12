"""
Some useful tools for the whole app: \n
Timer, 
"""

import functools
import typing as t
import time

class Timer(object):
    """
    Class to make timer decorators for VOID functions
    """
    dtime: float
    isabsolute: bool = False

    def timer(self, func: t.Callable):
        timer_mode: t.Callable = time.process_time
        if self.isabsolute:
            timer_mode = time.time
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = timer_mode()
            func(*args, **kwargs)
            end = timer_mode()
            self.dtime = end - start
        return wrapper

    def set_mode_absolute(self, isabsolute: bool = False):
        self.isabsolute = isabsolute

    def float_time(self) -> float:
        """
        Returns:
            float: last time measured by current instance of timer
        """
        return self.dtime

    def ddhhss_time(self) -> str:
        """
        Returns:
            str: last time measured by current instance of timer \n
            formatted in HH:MM:SS
        """
        return time.strftime("%H:%M:%S", time.gmtime(self.dtime))

# --- --- --- --- --- EXAMPLE

# timer = Timer()

# timer.set_mode_absolute(True)
# @timer.timer
# def waiter(timing: float):
#     time.sleep(timing)

# waiter(3)
# print(timer.ddhhss_time())

# waiter(2)
# print(timer.float_time())
