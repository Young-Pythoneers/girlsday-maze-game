import numpy as np

class Transition:
    def __init__(self, entity):
        self.entity = entity
        self.transition_function = None
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0

    def transition(self, event_listener, timer_keeper):
        ...

    def define_transition(self, transition_start_X, transition_start_Y, transition_goal_X, transition_goal_Y):
        self.transition_start_X = transition_start_X
        self.transition_start_Y = transition_start_Y
        self.transition_stop_X = transition_goal_X
        self.transition_stop_Y = transition_goal_Y

class LinearTransition(Transition):
    def __init__(self, entity):
        self.entity = entity
        self.transition_function = lambda x: x
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0

class CosTransition(Transition):
    def __init__(self, entity):
        self.entity = entity
        self.transition_function = lambda x: -np.cos(np.pi * x / 2) + 1
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0

    def transition(self, event_listener, timer_keeper):
        time_fraction = self.entity.entityKeeper.entityKeeper.transition_timer.timer / self.entity.entityKeeper.entityKeeper.transition_timer.timer_duration
        self.entity.X = self.transition_start_X + (
                    self.transition_stop_X - self.transition_start_X) * self.transition_function(time_fraction)
        self.entity.Y = self.transition_start_Y + (
                    self.transition_stop_Y - self.transition_start_Y) * self.transition_function(time_fraction)

class InstantTransition(Transition):
    def __init__(self, entity):
        self.entity = entity
        self.transition_function = None
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0

    def transition(self, event_listener, timer_keeper):
        time_fraction = self.entity.entityKeeper.entityKeeper.transition_timer.timer / self.entity.entityKeeper.entityKeeper.transition_timer.timer_duration
        self.entity.X = self.transition_stop_X
        self.entity.Y = self.transition_stop_Y