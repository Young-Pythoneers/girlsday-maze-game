import numpy as np
from girlsday_game.entity import GridEntity, Tile, Wall

class EntityKeeper:
    def __init__(self):
        self.entities = []

    def addEntity(self, ent):
        self.entities.append(ent)

    def removeEntity(self, ent):
        self.entities.remove(ent)

    def updateEntities(self, event_listener):
        for ent in self.entities:
            ent.update(event_listener)

class Grid(EntityKeeper):
    def __init__(self, size_X, size_Y):
        self.entities = []
        self.size_X = size_X
        self.size_Y = size_Y
        self.zero_X = 50
        self.zero_Y = 50
        self.tile_size = 50
        self.wall_size = 50
        self.transition_time = 0.3
        for i in range(self.size_Y):
            for j in range(self.size_X):
                self.addGridEntity(Tile(self), j, i)
        for i in range(2 * self.size_Y + 1):
            for j in range(2 * self.size_X + 1):
                self.addWall(Wall(self), j, i)

    def sub_grid_XY_to_world_XY(self, sub_grid_X, sub_grid_Y):
        X = (sub_grid_X // 2) * self.tile_size + np.ceil(sub_grid_X / 2) * self.wall_size + self.zero_X
        Y = (sub_grid_Y // 2) * self.tile_size + np.ceil (sub_grid_Y / 2) * self.wall_size + self.zero_Y
        return X, Y

    def set_sub_grid_to_world_XY(self, ent):
        ent.X, ent.Y = self.sub_grid_XY_to_world_XY(ent.sub_grid_X, ent.sub_grid_Y)

    def grid_XY_to_world_XY(self, grid_X, grid_Y):
        X = grid_X * self.tile_size + (grid_X + 1) * self.wall_size + self.zero_X
        Y = grid_Y * self.tile_size + (grid_Y + 1) * self.wall_size + self.zero_Y
        return X, Y

    def set_grid_XY_to_world_XY(self, ent):
        ent.X, ent.Y = self.grid_XY_to_world_XY(ent.grid_X, ent.grid_Y)

    def addGridEntity(self, ent, grid_X, grid_Y):
        ent.grid_X = grid_X
        ent.grid_Y = grid_Y
        ent.transition_time = self.transition_time
        self.entities.append(ent)
        self.set_grid_XY_to_world_XY(ent)

    def addWall(self, ent, sub_grid_X, sub_grid_Y):
        ent.sub_grid_X = sub_grid_X
        ent.sub_grid_Y = sub_grid_Y
        self.entities.append(ent)
        self.set_sub_grid_to_world_XY(ent)