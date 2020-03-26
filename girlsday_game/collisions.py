from girlsday_game.music import music
import itertools
import math

import numpy as np

from girlsday_game.entity import PhysicalEntity, Projectile

SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600


class Collisions:
    def collision(selfs, ent1, ent2):
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
        return output1 or output2

    def applyCollisions(self, entities):
        #For every PhysicalEntity, check if they go off the edge of the screen
        #If so, reverse the impulse
        for ent in entities:
            if isinstance(ent, PhysicalEntity):
                if ent.X < 0 or ent.X > SCREEN_SIZE_X - ent.X_size:
                    ent.impulse_X = -ent.impulse_X
                    ent.collided = True
                if ent.Y < 0 or ent.Y > SCREEN_SIZE_Y - ent.Y_size:
                    ent.impulse_Y = -ent.impulse_Y
                    ent.collided = True
                ent.X = np.clip(ent.X, 0, SCREEN_SIZE_X - ent.X_size)
                ent.Y = np.clip(ent.Y, 0, SCREEN_SIZE_Y - ent.Y_size)
        #For every pair of PhysicalEntities, check if they are in a collision
        #If so, they each give eachother a part of their impulse
        for ent1, ent2 in list(itertools.combinations(entities, 2)):
            if isinstance(ent1, PhysicalEntity) and isinstance(ent2, PhysicalEntity) and not (isinstance(ent1, Projectile) and isinstance(ent2, Projectile)):
                if self.collision(ent1, ent2):
                    impulse_X_dif = ent1.impulse_X - ent2.impulse_X
                    impulse_Y_dif = ent1.impulse_Y - ent2.impulse_Y
                    ent1.impulse_X = -impulse_X_dif
                    ent1.impulse_Y = -impulse_Y_dif
                    ent2.impulse_X = impulse_X_dif
                    ent2.impulse_Y = impulse_Y_dif
                    ent1.collided = True
                    ent2.collided = True
                    music.sound_handler('../sounds/buble_shot.wav', 0)
