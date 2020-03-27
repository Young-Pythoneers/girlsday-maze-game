import numpy as np
import math
from girlsday_game.entity import GridEntity, Tile, Wall, Player

class EntityKeeper:
    def __init__(self, game):
        self.game = game
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
    def __init__(self, game, entityKeeper, grid_X, grid_Y, zero_X, zero_Y, tile_size, wall_size):
        self.game = None #A gridpoint does not live inside of a game, but inside of a grid
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
    def __init__(self, game, timer_keeper):
        self.game = game
        self.entities = []
        self.size_X = 0
        self.size_Y = 0
        self.zero_X = 50
        self.zero_Y = 50
        self.tile_size = 50
        self.wall_size = 50
        self.transition_cooldown = 0.3
        self.transition_timer = timer_keeper.addTimer(0)
        self.in_transition = False #Are we in a transition state?
        self.play = False#Do we play all commands in the player's queue?
        self.player = None #can be removed in future
        self.input_cooldown = 0.3  # can be removed in future
        self.input_timer = timer_keeper.addTimer(0)# can be removed in future

        lvl1 = np.array([
            "wwwwwwwwwwwwwww",
            "wtntntntntntntw",
            "wnwwwwwwwwwwwnw",
            "wtwtntntntntwtw",
            "wnwnwwwwwwwnwnw",
            "wtwtwtntntntwtw",
            "wnwnwwwwwwwwwnw",
            "wtwtntntntntntw",
            "wwwwwwwwwwwwwww",
        ])

        self.size_X = len(lvl1[0])
        self.size_Y = len(lvl1)

        #Create the grid
        self.grid = []
        for i in range(self.size_Y):
            grid_row = []
            for j in range(self.size_X):
                gridPoint = GridPoint(self, None, j, i, self.zero_X, self.zero_Y, self.tile_size, self.wall_size)
                gridPoint.entityKeeper = self
                grid_row.append(gridPoint)
            self.grid.append(grid_row)

        self.all_walls = []

        # Fill the grid with Tiles and Walls
        for i in range(len(lvl1)):
            for j in range(len(lvl1[i])):
                single_letter = lvl1[i][j]

                if single_letter == "w":
                    self.addGridEntity(Wall(self.grid[i][j]), j, i)
                    self.all_walls.append([j, i])
                elif single_letter == "t":
                    self.addGridEntity(Tile(self.grid[i][j]), j, i)
                elif single_letter == "n":
                    pass



    def addGridEntity(self, ent, grid_X, grid_Y):
        if isinstance(ent, Player):
            self.player = ent
        self.entities.append(ent)
        self.grid[grid_Y][grid_X].addEntity(ent)
        self.grid[grid_Y][grid_X].set_grid_XY_to_world_XY(ent)

    def removeGridEntity(self, ent):
        ent.entityKeeper.removeEntity(ent)
        self.entities.remove(ent)

    def updateEntities(self, event_listener, timer_keeper):
        #Check the event_listener to see if there is keyboard input
        if self.input_timer.check_timer() and not self.play  and (event_listener.K_LEFT or event_listener.K_RIGHT or event_listener.K_UP or event_listener.K_DOWN):
            X_change = 0
            Y_change = 0
            if event_listener.K_LEFT:
                X_change -= 2
            if event_listener.K_RIGHT:
                X_change += 2
            if event_listener.K_UP:
                Y_change -= 2
            if event_listener.K_DOWN:
                Y_change += 2
            #If there is input, apply the input by putting a command on the player's queue
            self.player.command_queue.append((X_change, Y_change))
            #Set the input_cooldown_timer to better separate individual key presses
            self.input_timer = timer_keeper.addTimer(self.input_cooldown)

        #Check if we did not allready start a transition and we are in play mode.
        #If the space bar is pressed when not in a transition, we want to start the play mode.
        #We should not be in the transition mode, because a new transition is initialized
        #A currently running transition should first finish
        if not self.in_transition and (event_listener.K_SPACE or self.play):
            #Set behaviour to play mode. The player can end the play mode once its commands queue is empty
            self.play = True
            #Begin a new transition phase
            self.begin_transition(timer_keeper)

        #If we are in a transition manage its timer and check if the transition should be stopped
        if self.transition_timer.check_timer() and self.in_transition:
                self.end_transition(timer_keeper)

        #Ask all entities to update their world coordinates and to do whatever they do
        for ent in self.entities:
            ent.update(event_listener, timer_keeper)


    def moveGridEntity(self, ent, destination_X, destination_Y):
        ent.entityKeeper.removeEntity(ent)
        self.grid[destination_Y][destination_X].addEntity(ent)

    def requestMove(self, grid_source_X, grid_source_Y, grid_destination_X, grid_destination_Y):
        #TODO Nathan BEGIN
        #Nathan: voordat een entity zich naar een nieuw GridPoint verplaatst, vraagt hij aan grid of dit wel kan / mag
        #Voor nu wordt er alleen gekeken of een entity niet van de grid afloopt
        #Je dit kunnen uitbreiden door te kijken of er een wall tussen de source en destination zit
        #TODO Nathan END
        #print(self.grid[grid_destination_Y][grid_destination_X])

        self.player_with_in_grid = grid_destination_X >= 0 and grid_destination_X < self.size_X and grid_destination_Y >= 0 and grid_destination_Y < self.size_Y
        self.player_wall_collsion = [(grid_destination_X + grid_source_X)/2, (grid_destination_Y + grid_source_Y)/2] in self.all_walls

        if self.player_wall_collsion == True:
            self.player_wall_collsion = False
        else:
            self.player_wall_collsion = True

        return self.player_with_in_grid and self.player_wall_collsion



    def begin_transition(self, timer_keeper):
        self.transition_timer = timer_keeper.addTimer(self.transition_cooldown)
        self.in_transition = True
        for ent in self.entities:
            if isinstance(ent, GridEntity):
                ent.begin_transition()

    def end_transition(self, timer_keeper):
        self.in_transition = False
        for ent in self.entities:
            if isinstance(ent, GridEntity):
                ent.end_transition(timer_keeper)