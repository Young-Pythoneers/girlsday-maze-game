from girlsday_game.timer import Timer

from time import time

class TimerKeeper:
    def __init__(self):
        self.timers = []
        self.previous_time = time()
        self.current_time = time()
        self.time_passed = self.current_time - self.previous_time

    def add_timer(self, timer_duration):
        timer = Timer(timer_duration,self)
        self.timers.append(timer)
        return timer

    def remove_timer(self,timer):
        self.timers.remove(timer)

    def update_timers(self):
        self.previous_time = self.current_time
        self.current_time = time()
        self.time_passed = self.current_time - self.previous_time
        for timer in self.timers:
            timer.update(self.time_passed)