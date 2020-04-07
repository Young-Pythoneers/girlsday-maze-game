from time import time


class Timer:
    def __init__(self, timer_duration):
        self.timer = 0
        self.timer_duration = timer_duration
        self.timer_container = None
        self.destroyed = False

    def update(self, time_passed):
        if self.timer >= self.timer_duration:
            self.destruct()
        self.timer += time_passed

    def check_timer(self):
        return self.destroyed

    def destruct(self):
        self.destroyed = True
        self.timer_container.remove(self)


class TimerContainer:
    def __init__(self):
        self.timers = []
        self.previous_time = time()
        self.current_time = time()
        self.time_passed = self.current_time - self.previous_time

    def append(self, timer):
        timer.timer_container = self
        self.timers.append(timer)

    def remove(self, timer):
        self.timers.remove(timer)

    def update_timers(self):
        self.previous_time = self.current_time
        self.current_time = time()
        self.time_passed = self.current_time - self.previous_time
        for timer in self.timers:
            timer.update(self.time_passed)
