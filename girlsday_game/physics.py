from typing import List

from girlsday_game.entity import Entity, PhysicalEntity
from girlsday_game.listener import EventListener
from girlsday_game.timer import TimerContainer


class Physics:
    """ Class that applies physics to PhysicalEntities

    Attributes:
        game (Game): The game this Physics object lives in
        friction (int): The amount of friction to apply in an arbitrary unit
        grafity (int): The amount of gravity to apply in an arbitrary unit
    """

    def __init__(self, game):
        self.game = game
        self.friction = 3
        self.gravity = 10

    def apply_physics(
        self,
        entities: List[Entity],
        event_listener: EventListener,
        timer_keeper: TimerContainer,
    ) -> None:
        """ Function that applies the following physical effects to PhysicalEntities only:
        friction, gravity and kinetic energy.

        Args:
            entities: All entities in the game
            event_listener: The event listener that listens for keyboard input
            timer_keeper: The timer keeper that tracks all timers
        """
        for ent in entities:
            # Only apply Physics to PhysicalEntities
            if isinstance(ent, PhysicalEntity):
                # Apply friction
                # The higher the mass, the less effect friction has.
                ent.impulse_x /= (
                    1 + (self.friction * timer_keeper.time_passed) / ent.mass
                )
                ent.impulse_y /= (
                    1 + (self.friction * timer_keeper.time_passed) / ent.mass
                )
                if (
                    ent.y <= self.game.display.screen_size_y - ent.y_size
                ):  # This if statement fixes weird behaviour at the screen's bottom.
                    # Apply gravity
                    ent.impulse_y += self.gravity * ent.mass * timer_keeper.time_passed
                # Update the Entity's position acording to its impulse (kinetic energy) and mass.
                # The higher the mass, the more impulse is needed for movement.
                ent.x += ent.impulse_x / ent.mass
                ent.y += ent.impulse_y / ent.mass
