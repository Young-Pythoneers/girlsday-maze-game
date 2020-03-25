import numpy as np
from girlsday_game.entity import GridEntity, Tile, Wall

class EntityKeeper:
    def __init__(self):
        self.entities = []

    def addEntity(self, ent):
        ent.entityKeeper = self
        self.entities.append(ent)

    def removeEntity(self, ent):
        ent.entityKeeper = None
        self.entities.remove(ent)

    def updateEntities(self, event_listener):
        for ent in self.entities:
            ent.update(event_listener)

class GridPoint(EntityKeeper):
    def __init__(self, entityKeeper, grid_X, grid_Y, zero_X, zero_Y, tile_size, wall_size):
        self.entities = []
        self.entityKeeper = entityKeeper
        self.grid_X = grid_X
        self.grid_Y = grid_Y
        self.zero_X = zero_X
        self.zero_Y = zero_Y
        self.tile_size = tile_size
        self.wall_size = wall_size

    def grid_XY_to_world_XY(self, grid_X, grid_Y):
        X = (grid_X // 2) * self.tile_size + np.ceil(grid_X / 2) * self.wall_size + self.zero_X
        Y = (grid_Y // 2) * self.tile_size + np.ceil (grid_Y / 2) * self.wall_size + self.zero_Y
        return X, Y

    def set_grid_XY_to_world_XY(self, ent):
        ent.X, ent.Y = self.grid_XY_to_world_XY(self.grid_X, self.grid_Y)

class Grid(EntityKeeper):
    def __init__(self, size_X, size_Y):
        self.entities = []
        self.size_X = size_X
        self.size_Y = size_Y
        self.zero_X = 50
        self.zero_Y = 50
        self.tile_size = 50
        self.wall_size = 50
        self.transition_time_counter = 0
        self.transition_time = 0.3
        self.in_transition = False
        self.grid = []
        for i in range(self.size_Y):
            grid_row = []
            for j in range(self.size_X):
                gridPoint = GridPoint(self, j, i, self.zero_X, self.zero_Y, self.tile_size, self.wall_size)
                gridPoint.entityKeeper = self
                grid_row.append(gridPoint)
            self.grid.append(grid_row)

        for i in range(self.size_Y // 2):
            for j in range(self.size_X // 2):
                self.addGridEntity(Tile(), j * 2 + 1, i * 2 + 1)
        for i in range(self.size_Y):
            for j in range(self.size_X):
                self.addGridEntity(Wall(), j, i)

    def addGridEntity(self, ent, grid_X, grid_Y):
        ent.transition_time = self.transition_time
        self.entities.append(ent)
        self.grid[grid_Y][grid_X].addEntity(ent)
        self.grid[grid_Y][grid_X].set_grid_XY_to_world_XY(ent)

    def removeGridEntity(self, ent):
        ent.entityKeeper.removeEntity(ent)
        self.entities.remove(ent)

    def updateEntities(self, event_listener):
        for ent in self.entities:
            ent.update(event_listener)
        self.transition_time_counter += event_listener.time_passed
        if self.transition_time_counter >= self.transition_time:
            self.end_transition()


    def moveGridEntity(self, ent, destination_X, destination_Y):
        ent.entityKeeper.removeEntity(ent)
        self.grid[destination_Y][destination_X].addEntity(ent)

    def requestMove(self, grid_destination_X, grid_destination_Y):
        self.define_transition()
        return grid_destination_X >= 0 and grid_destination_X < self.size_X and grid_destination_Y >= 0 and grid_destination_Y < self.size_Y

    def define_transition(self):
        self.transition_time_counter = 0
        self.in_transition = True

    def end_transition(self):
        self.in_transition = False
        for ent in self.entities:
            ent.entityKeeper.set_grid_XY_to_world_XY(ent)