import itertools
import math

import numpy as np

from girlsday_game.entity import Collider, Particle, PhysicalEntity


class Collisions:
    def __init__(self, game):
        self.game = game

    def collision(selfs, ent1, ent2):
        penetration = 0
        distance = math.sqrt(
            math.pow(ent1.x - ent2.x, 2) + math.pow(ent1.y - ent2.y, 2)
        )
        if distance > 50:
            return False
        points1 = [
            (ent1.x, ent1.y),
            (ent1.x + ent1.x_size, ent1.y),
            (ent1.x + ent1.x_size, ent1.y + ent1.y_size),
            (ent1.x, ent1.y + ent1.y_size),
        ]
        points2 = [
            (ent2.x, ent2.y),
            (ent2.x + ent2.x_size, ent2.y),
            (ent2.x + ent2.x_size, ent2.y + ent2.y_size),
            (ent2.x, ent2.y + ent2.y_size),
        ]
        output1 = any(
            [
                p[0] >= ent2.x
                and p[0] <= ent2.x + ent2.x_size
                and p[1] >= ent2.y
                and p[1] <= ent2.y + ent2.y_size
                for p in points1
            ]
        )
        output2 = any(
            [
                p[0] >= ent1.x
                and p[0] <= ent1.x + ent1.x_size
                and p[1] >= ent1.y
                and p[1] <= ent1.y + ent1.y_size
                for p in points2
            ]
        )
        return output1 or output2

    def apply_collisions(self, entities):
        # For every PhysicalEntity, check if they go off the edge of the screen
        # If so, reverse the impulse
        for ent in entities:
            if isinstance(ent, PhysicalEntity):
                if ent.x < 0 or ent.x > self.game.display.screen_size_x - ent.x_size:
                    ent.impulse_x = -ent.impulse_x
                if ent.y < 0 or ent.y > self.game.display.screen_size_y - ent.y_size:
                    ent.impulse_y = -ent.impulse_y
                ent.x = np.clip(ent.x, 0, self.game.display.screen_size_x - ent.x_size)
                ent.y = np.clip(ent.y, 0, self.game.display.screen_size_y - ent.y_size)
        # For every pair of PhysicalEntities, check if they are in a collision
        # If so, they each give eachother a part of their impulse
        for ent1, ent2 in list(itertools.combinations(entities, 2)):
            if isinstance(ent1, Collider) and isinstance(ent2, Collider):
                collided = self.collision(ent1, ent2)
                if collided:
                    ent1.register_collision(ent2)
                    ent2.register_collision(ent1)

        for ent in entities:
            if isinstance(ent, Collider):
                ent.update_collisions()
