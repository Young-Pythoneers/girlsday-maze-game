class Timer:
    def __init__(self, timer_duration, timer_keeper):
        self.timer = 0
        self.timer_duration = timer_duration
        self.timer_keeper = timer_keeper
        self.destroyed = False

    def update(self, time_passed):
        if self.timer >= self.timer_duration:
            self.destruct()
        self.timer += time_passed

    def check_timer(self):
        return self.destroyed

    def destruct(self):
        self.destroyed = True
        self.timer_keeper.remove_timer(self)