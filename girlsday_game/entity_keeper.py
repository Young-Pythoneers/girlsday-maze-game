import numpy as np
import math
from girlsday_game.entity import GridEntity, Tile, Wall, Player

class EntityKeeper:
    def __init__(self):
        self.entities = []

    def add_entity(self, ent):
        ent.entity_keeper = self
        self.entities.append(ent)

    def remove_entity(self, ent):
        ent.entity_keeper = None
        self.entities.remove(ent)

    def update_entities(self, event_listener):
        for ent in self.entities:
            ent.update(event_listener)

class GridPoint(EntityKeeper):
    def __init__(self, entity_keeper, grid_x, grid_y, zero_x, zero_y, tile_size, wall_size):
        EntityKeeper.__init__(self)
        self.entity_keeper = entity_keeper
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.zero_x = zero_x
        self.zero_y = zero_y
        self.tile_size = tile_size
        self.wall_size = wall_size

    def grid_xy_to_world_xy(self, grid_x, grid_y):
        x = (grid_x // 2) * self.tile_size + np.ceil(grid_x / 2) * self.wall_size + self.zero_x
        y = (grid_y // 2) * self.tile_size + np.ceil (grid_y / 2) * self.wall_size + self.zero_y
        return x, y

    def set_grid_xy_to_world_xy(self, ent):
        ent.x, ent.y = self.grid_xy_to_world_xy(self.grid_x, self.grid_y)

class Grid(EntityKeeper):
    def __init__(self, timer_keeper):
        EntityKeeper.__init__(self)
        self.size_x = 0
        self.size_y = 0
        self.zero_x = 50
        self.zero_y = 50
        self.tile_size = 50
        self.wall_size = 50
        self.transition_cooldown = 0.3
        self.transition_timer = timer_keeper.add_timer(0)
        self.in_transition = False #Are we in a transition state?
        self.play = False#Do we play all commands in the player's queue?
        self.player = None #can be removed in future
        self.input_cooldown = 0.1  # can be removed in future
        self.input_timer = timer_keeper.add_timer(0)# can be removed in future
        
        level = self.load_level()
        self.create_grid(level)
        
    def load_level(self):
        level= np.array([
            "wwwwwwwwwwwwwww",
            "wtntntntntntntw",
            "wnwwwwwnwwwwwnw",
            "wtwtntntwtntwtw",
            "wnwnwwwwwwwnwnw",
            "wtntwtntntntwtw",
            "wnnnwwwwwnnnwnw",
            "wtntntntntntntw",
            "wwwwwwwwwwwwwww",
        ])
        return level


    def create_grid(self, level):
        self.size_x = len(level[0])
        self.size_y = len(level)

        #Create the grid
        self.grid = []
        for i in range(self.size_y):
            grid_row = []
            for j in range(self.size_x):
                gridPoint = GridPoint(self, j, i, self.zero_x, self.zero_y, self.tile_size, self.wall_size)
                gridPoint.entity_keeper = self
                grid_row.append(gridPoint)
            self.grid.append(grid_row)

        self.all_walls = []

        # Fill the grid with Tiles and Walls
        for i in range(len(level)):
            for j in range(len(level[i])):
                single_letter = level[i][j]

                if single_letter == "w":
                    self.add_grid_entity(Wall(self.grid[i][j]), j, i)
                    self.all_walls.append([j, i])
                elif single_letter == "t":
                    self.add_grid_entity(Tile(self.grid[i][j]), j, i)
                elif single_letter == "n":
                    pass


    def add_grid_entity(self, ent, grid_x, grid_y):
        if isinstance(ent, Player):
            self.player = ent
        self.entities.append(ent)
        self.grid[grid_y][grid_x].add_entity(ent)
        self.grid[grid_y][grid_x].set_grid_xy_to_world_xy(ent)

    def remove_grid_entity(self, ent):
        ent.entity_keeper.remove_entity(ent)
        self.entities.remove(ent)

    def check_input(self, event_listener):
        x_change = 0
        y_change = 0
        if event_listener.K_LEFT:
            x_change -= 2
        if event_listener.K_RIGHT:
            x_change += 2
        if event_listener.K_UP:
            y_change -= 2
        if event_listener.K_DOWN:
            y_change += 2
        return x_change, y_change

    def update_entities(self, event_listener, timer_keeper):
        #Check the event_listener to see if there is keyboard input
        if self.input_timer.check_timer() and not self.play  and (event_listener.K_LEFT or event_listener.K_RIGHT or event_listener.K_UP or event_listener.K_DOWN):
            x_change, y_change = self.check_input(event_listener)
            #If there is input, apply the input by putting a command on the player's queue
            self.player.command_queue.append((x_change, y_change))
            #Set the input_cooldown_timer to better separate individual key presses
            self.input_timer = timer_keeper.add_timer(self.input_cooldown)

        #Check if we did not allready start a transition and we are in play mode.
        #If the space bar is pressed when not in a transition, we want to start the play mode.
        #We should not be in the transition mode, because a new transition is initialized
        #A currently running transition should first finish
        if not self.in_transition and (event_listener.K_SPACE or self.play):
            #Set behaviour to play mode. The player can end the play mode once its commands queue is empty
            self.play = self.begin_transition(timer_keeper)

        #If we are in a transition manage its timer and check if the transition should be stopped
        if self.transition_timer.check_timer() and self.in_transition:
                self.end_transition(timer_keeper)

        #Ask all entities to update their world coordinates and to do whatever they do
        for ent in self.entities:
            ent.update(event_listener, timer_keeper)


    def move_grid_entity(self, ent, destination_x, destination_y):
        ent.entity_keeper.remove_entity(ent)
        self.grid[destination_y][destination_x].add_entity(ent)

    def request_move(self, grid_source_x, grid_source_y, grid_destination_x, grid_destination_y):
        #TODO Nathan BEGIN
        #Nathan: voordat een entity zich naar een nieuw GridPoint verplaatst, vraagt hij aan grid of dit wel kan / mag
        #Voor nu wordt er alleen gekeken of een entity niet van de grid afloopt
        #Je dit kunnen uitbreiden door te kijken of er een wall tussen de source en destination zit
        #TODO Nathan END
        #print(self.grid[grid_destination_y][grid_destination_x])

        self.player_with_in_grid = 0 <= grid_destination_x < self.size_x and 0 <= grid_destination_y < self.size_y
        self.player_wall_collsion = [(grid_destination_x + grid_source_x)/2, (grid_destination_y + grid_source_y)/2] in self.all_walls

        return self.player_with_in_grid and not self.player_wall_collsion



    def begin_transition(self, timer_keeper):
        if len(self.player.command_queue) <= 0:
            return False
        self.transition_timer = timer_keeper.add_timer(self.transition_cooldown)
        self.in_transition = True
        for ent in self.entities:
            if isinstance(ent, GridEntity):
                ent.begin_transition()
        return True

    def end_transition(self, timer_keeper):
        self.in_transition = False
        for ent in self.entities:
            if isinstance(ent, GridEntity):
                ent.end_transition(timer_keeper)