import numpy as np

from girlsday_game.entity import PhysicalEntity

SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600


class Physics:
    def __init__(self):
        self.friction = 3
        self.gravity = 0

    def applyPhysics(self, entities, event_listener):
        for ent in entities:
            if isinstance(ent, PhysicalEntity):
                ent.impulse_X /= (
                    1 + (self.friction * event_listener.time_passed) / ent.mass
                )
                ent.impulse_Y /= (
                    1 + (self.friction * event_listener.time_passed) / ent.mass
                )
                if ent.Y <= SCREEN_SIZE_Y - ent.Y_size:
                    ent.impulse_Y += (
                        self.gravity * ent.mass * event_listener.time_passed
                    )
                ent.X += ent.impulse_X / ent.mass
                ent.Y += ent.impulse_Y / ent.mass
