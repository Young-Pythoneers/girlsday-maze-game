from girlsday_game.music import music
import itertools
import math

import numpy as np

from girlsday_game.entity import PhysicalEntity, Projectile, Tile, Player, Goal, Wall, Score

class Collisions:
    def __init__(self, game):
        self.game = game

    def collision(selfs, ent1, ent2):
        penetration = 0
        distance = math.sqrt(math.pow(ent1.x - ent2.x, 2) + math.pow(ent1.y - ent2.y, 2))
        if  distance > 50:
            return False, 0
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
        return output1 or output2, distance

    def apply_collisions(self, entities):
        #For every PhysicalEntity, check if they go off the edge of the screen
        #If so, reverse the impulse
        for ent in entities:
            if isinstance(ent, PhysicalEntity):
                if ent.x < 0 or ent.x > self.game.display.screen_size_x - ent.x_size:
                    ent.impulse_x = -ent.impulse_x
                    ent.collided = True
                if ent.y < 0 or ent.y > self.game.display.screen_size_y - ent.y_size:
                    ent.impulse_y = -ent.impulse_y
                    ent.collided = True
                ent.x = np.clip(ent.x, 0, self.game.display.screen_size_x - ent.x_size)
                ent.y = np.clip(ent.y, 0, self.game.display.screen_size_y - ent.y_size)
        #For every pair of PhysicalEntities, check if they are in a collision
        #If so, they each give eachother a part of their impulse
        for ent1, ent2 in list(itertools.combinations(entities, 2)):
            if (not (isinstance(ent1, Projectile) and isinstance(ent2, Projectile)) and
                    (not (isinstance(ent1, Tile) or isinstance(ent2, Tile))) and
                    (not (isinstance(ent1, Player) or isinstance(ent2, Player))) and
                    (not (isinstance(ent1, Goal) or isinstance(ent2, Goal))) and
                    (not (isinstance(ent1, Score) or isinstance(ent2, Score)))):
                collided, distance = self.collision(ent1, ent2)
                if collided:
                    if isinstance(ent1, PhysicalEntity):
                        x1 = ent1.impulse_x
                        y1 = ent1.impulse_y
                    else:
                        x1 = 0
                        y1 = 0
                    if isinstance(ent2, PhysicalEntity):
                        x2 = ent2.impulse_x
                        y2 = ent2.impulse_y
                    else:
                        x2 = 0
                        y2 = 0
                    impulse_x_dif = x1 - x2
                    impulse_y_dif = y1 - y2
                    if isinstance(ent1, PhysicalEntity):
                        ent1.impulse_x = -impulse_x_dif
                        ent1.impulse_y = -impulse_y_dif
                        ent1.collided = True
                    if isinstance(ent2, PhysicalEntity):
                        ent2.impulse_x = impulse_x_dif
                        ent2.impulse_y = impulse_y_dif
                        ent2.collided = True
