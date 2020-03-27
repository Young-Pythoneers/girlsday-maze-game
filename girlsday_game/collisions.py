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
        distance = math.sqrt(math.pow(ent1.X - ent2.X, 2) + math.pow(ent1.Y - ent2.Y, 2))
        if  distance > 50:
            return False, 0
        points1 = [
            (ent1.X, ent1.Y),
            (ent1.X + ent1.X_size, ent1.Y),
            (ent1.X + ent1.X_size, ent1.Y + ent1.Y_size),
            (ent1.X, ent1.Y + ent1.Y_size),
        ]
        points2 = [
            (ent2.X, ent2.Y),
            (ent2.X + ent2.X_size, ent2.Y),
            (ent2.X + ent2.X_size, ent2.Y + ent2.Y_size),
            (ent2.X, ent2.Y + ent2.Y_size),
        ]
        output1 = any(
            [
                p[0] >= ent2.X
                and p[0] <= ent2.X + ent2.X_size
                and p[1] >= ent2.Y
                and p[1] <= ent2.Y + ent2.Y_size
                for p in points1
            ]
        )
        output2 = any(
            [
                p[0] >= ent1.X
                and p[0] <= ent1.X + ent1.X_size
                and p[1] >= ent1.Y
                and p[1] <= ent1.Y + ent1.Y_size
                for p in points2
            ]
        )
        return output1 or output2, distance

    def applyCollisions(self, entities):
        #For every PhysicalEntity, check if they go off the edge of the screen
        #If so, reverse the impulse
        for ent in entities:
            if isinstance(ent, PhysicalEntity):
                if ent.X < 0 or ent.X > self.game.display.screen_size_X - ent.X_size:
                    ent.impulse_X = -ent.impulse_X
                    ent.collided = True
                if ent.Y < 0 or ent.Y > self.game.display.screen_size_Y - ent.Y_size:
                    ent.impulse_Y = -ent.impulse_Y
                    ent.collided = True
                ent.X = np.clip(ent.X, 0, self.game.display.screen_size_X - ent.X_size)
                ent.Y = np.clip(ent.Y, 0, self.game.display.screen_size_Y - ent.Y_size)
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
                        X1 = ent1.impulse_X
                        Y1 = ent1.impulse_Y
                    else:
                        X1 = 0
                        Y1 = 0
                    if isinstance(ent2, PhysicalEntity):
                        X2 = ent2.impulse_X
                        Y2 = ent2.impulse_Y
                    else:
                        X2 = 0
                        Y2 = 0
                    impulse_X_dif = X1 - X2
                    impulse_Y_dif = Y1 - Y2
                    if isinstance(ent1, PhysicalEntity):
                        ent1.impulse_X = -impulse_X_dif
                        ent1.impulse_Y = -impulse_Y_dif
                        ent1.collided = True
                    if isinstance(ent2, PhysicalEntity):
                        ent2.impulse_X = impulse_X_dif
                        ent2.impulse_Y = impulse_Y_dif
                        ent2.collided = True
