class Timer:
    def __init__(self, timer_duration, timer_keeper):
        self.timer = 0
        self.timer_duration = timer_duration
        self.timer_keeper = timer_keeper
        self.destroyed = False

    def update(self, time_passed):
        self.timer += time_passed

    def check_timer(self):
        if self.destroyed:
            return True
        if self.timer >= self.timer_duration:
            self.destruct()
            self.destroyed = True
            return True
        else:
            return False

    def destruct(self):
        self.timer_keeper.removeTimer(self)