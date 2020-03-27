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

    def define_transition(self, grid_destination_X, grid_destination_Y):
        # Check if the transition to the destination is possible
        if not self.entity.entityKeeper.entityKeeper.requestMove(self.entity.entityKeeper.grid_X, self.entity.entityKeeper.grid_Y,
                                                          grid_destination_X, grid_destination_Y):
            # If the transition is not possible, a transition is still initialized, but with a change of 0.
            # This way this entity is not moved, but it still waits for one transition interval.
            # This is needed to synchronize all transitioning entities.
            grid_destination_X = self.entity.entityKeeper.grid_X
            grid_destination_Y = self.entity.entityKeeper.grid_Y
        # Register the new grid position for the move
        self.entity.entityKeeper.entityKeeper.moveGridEntity(self.entity, grid_destination_X, grid_destination_Y)
        self.transition_start_X, self.transition_start_Y = self.entity.X, self.entity.Y
        # Calculate the destination in world coordinates
        self.transition_stop_X, self.transition_stop_Y = self.entity.entityKeeper.grid_XY_to_world_XY(grid_destination_X, grid_destination_Y)

class LinearTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self,entity)
        self.transition_function = lambda x: x

class CosTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)
        self.transition_function = lambda x: -np.cos(np.pi * x / 2) + 1

    def transition(self, event_listener, timer_keeper):
        time_fraction = self.entity.entityKeeper.entityKeeper.transition_timer.timer / self.entity.entityKeeper.entityKeeper.transition_timer.timer_duration
        self.entity.X = self.transition_start_X + (
                    self.transition_stop_X - self.transition_start_X) * self.transition_function(time_fraction)
        self.entity.Y = self.transition_start_Y + (
                    self.transition_stop_Y - self.transition_start_Y) * self.transition_function(time_fraction)

class WobblyTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)
        self.transition_function = lambda x: -np.cos(np.pi * x / 2) + 1

    def transition(self, event_listener, timer_keeper):
        time_fraction = self.entity.entityKeeper.entityKeeper.transition_timer.timer / self.entity.entityKeeper.entityKeeper.transition_timer.timer_duration
        self.entity.X = self.transition_start_X + (
                    self.transition_stop_X - self.transition_start_X) * self.transition_function(time_fraction)
        self.entity.Y = self.transition_start_Y + (
                    self.transition_stop_Y - self.transition_start_Y) * self.transition_function(time_fraction) + np.sin(np.pi * 4 * time_fraction) * 8

class InstantTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)
        self.transition_function = None

    def transition(self, event_listener, timer_keeper):
        time_fraction = self.entity.entityKeeper.entityKeeper.transition_timer.timer / self.entity.entityKeeper.entityKeeper.transition_timer.timer_duration
        self.entity.X = self.transition_stop_X
        self.entity.Y = self.transition_stop_Y