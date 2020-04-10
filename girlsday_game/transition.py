from abc import ABC, abstractmethod

import numpy as np


class Transition(ABC):
    def __init__(self, entity):
        self.entity = entity
        self.transition_start_x = 0
        self.transition_start_y = 0
        self.transition_stop_x = 0
        self.transition_stop_y = 0

    def transition_function(self, x):
        ...

    def transition(self, event_listener, timer_container):
        time_fraction = (
            self.entity.entity_container.entity_container.transition_timer.timer
            / self.entity.entity_container.entity_container.transition_timer.timer_duration
        )
        self.entity.rect.centerx = self.transition_start_x + (
            self.transition_stop_x - self.transition_start_x
        ) * self.transition_function(time_fraction)
        self.entity.rect.centery = self.transition_start_y + (
            self.transition_stop_y - self.transition_start_y
        ) * self.transition_function(time_fraction)

    def define_transition(self, grid_destination_x, grid_destination_y):
        # Check if the transition to the destination is possible
        if not self.entity.entity_container.entity_container.request_move(
            self.entity.entity_container.grid_x,
            self.entity.entity_container.grid_y,
            grid_destination_x,
            grid_destination_y,
        ):
            # If the transition is not possible, a transition is still initialized, but with a change of 0.
            # This way this entity is not moved, but it still waits for one transition interval.
            # This is needed to synchronize all transitioning entities.
            grid_destination_x = self.entity.entity_container.grid_x
            grid_destination_y = self.entity.entity_container.grid_y
        # Register the new grid position for the move
        self.entity.entity_container.entity_container.move_grid_entity(
            self.entity, grid_destination_x, grid_destination_y
        )
        self.transition_start_x, self.transition_start_y = self.entity.rect.centerx, self.entity.rect.centery
        # Calculate the destination in world coordinates
        (
            self.transition_stop_x,
            self.transition_stop_y,
        ) = self.entity.entity_container.grid_xy_to_world_xy(
            grid_destination_x, grid_destination_y
        )


class LinearTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)

    def transition_function(self, x):
        return x


class CosTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)

    def transition_function(self, x):
        return -np.cos(np.pi * x / 2) + 1

class WobblyTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)

    def transition_function(self, x):
        return -np.cos(np.pi * x / 2) + 1

    def transition(self, event_listener, timer_container):
        time_fraction = (
            self.entity.entity_container.entity_container.transition_timer.timer
            / self.entity.entity_container.entity_container.transition_timer.timer_duration
        )
        self.entity.rect.centerx = self.transition_start_x + (
            self.transition_stop_x - self.transition_start_x
        ) * self.transition_function(time_fraction)
        self.entity.rect.centery = (
            self.transition_start_y
            + (self.transition_stop_y - self.transition_start_y)
            * self.transition_function(time_fraction)
            + np.sin(np.pi * 4 * time_fraction) * 8
        )


class InstantTransition(Transition):
    def __init__(self, entity):
        Transition.__init__(self, entity)

    def transition_function(self, x):
        return 1.0

    def transition(self, event_listener, timer_container):
        self.entity.rect.centerx = self.transition_stop_x
        self.entity.rect.centery = self.transition_stop_y
