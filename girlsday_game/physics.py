import numpy as np

from girlsday_game.entity import Entity, PhysicalEntity
from girlsday_game.listener import EventListener

SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600


class Physics:
    """ Class that applies physics to PhysicalEntities

    Attributes:
        friction (int): The amount of friction to apply in an arbitrary unit
        grafity (int): The amount of gravity to apply in an arbitrary unit
    """

    def __init__(self):
        self.friction = 3
        self.gravity = 0

    def applyPhysics(self, entities: Entity, event_listener: EventListener) -> None:
        """ Function that applies the following physical effects to PhysicalEntities only:
        friction, gravity and kinetic energy.

        Args:
            entities (Entity): All entities in the game
            event_listener (EventListener): The event listener that listens for keyboard input

        Returns:
            None
        """
        for ent in entities:
            #Only apply Physics to PhysicalEntities
            if isinstance(ent, PhysicalEntity):
                #Apply friction
                #The higher the mass, the less effect friction has.
                ent.impulse_X /= (
                    1 + (self.friction * event_listener.time_passed) / ent.mass
                )
                ent.impulse_Y /= (
                    1 + (self.friction * event_listener.time_passed) / ent.mass
                )
                if ent.Y <= SCREEN_SIZE_Y - ent.Y_size:#This if statement fixes weird behaviour at the screen's bottom.
                    #Apply gravity
                    ent.impulse_Y += (
                        self.gravity * ent.mass * event_listener.time_passed
                    )
                #Update the Entity's position acording to its impulse (kinetic energy) and mass.
                #The higher the mass, the more impulse is needed for movement.
                ent.X += ent.impulse_X / ent.mass
                ent.Y += ent.impulse_Y / ent.mass
