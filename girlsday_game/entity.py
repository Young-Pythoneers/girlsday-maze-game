from __future__ import annotations

import math

import numpy as np
import pygame
from numpy.random import uniform

from girlsday_game.music import Music
from girlsday_game.timer import Timer, TimerContainer
from girlsday_game.transition import CosTransition, WobblyTransition
from girlsday_game.timer import Timer, TimerContainer


class Entity:
    def __init__(self, entity_container: EntityContainer = None):
        self.entity_container = entity_container
        self.x = 0
        self.y = 0
        self.image = None
        self.x_size = 0
        self.y_size = 0

    def give_center_xy(self):
        x = self.x - self.x_size / 2
        y = self.y - self.y_size / 2
        return x, y


class Commandable:
    def __init__(self):
        self.command_queue = []# TODO Replace this by a Program instance in the future


class Updateable:
    def update(self, event_listener, timer_container):
        ...


class Transitional:
    def __init__(self):
        self.transition = None

    def begin_transition(self):
        ...

    def end_transition(self, timer_container: TimerContainer):
        self.entity_container.set_grid_xy_to_world_xy(self)


class Collider:
    def __init__(self):
        self._collisions = []
        self._impulse_list = []
        self._does_not_collide_with = []

    def register_collision(self, collider):
        if not any([isinstance(collider, ent) for ent in self._does_not_collide_with]):
            self._collisions.append(collider)
            if isinstance(self, Physical):
                if isinstance(collider, Physical):
                    impulse_x_dif = self.impulse_x - collider.impulse_x
                    impulse_y_dif = self.impulse_y - collider.impulse_y
                else:
                    impulse_x_dif = 2 * self.impulse_x
                    impulse_y_dif = 2 * self.impulse_y
                self._impulse_list.append((impulse_x_dif, impulse_y_dif))

    def update_collisions(self):
        if isinstance(self, Physical):
            for impulse in self._impulse_list:
                self.impulse_x -= impulse[0]
                self.impulse_y -= impulse[1]
        self._impulse_list = []
        self._collisions = []



class Physical:
    def __init__(self, x, y, impulse_x, impulse_y):
        self.x = x
        self.y = y
        self.impulse_x = impulse_x
        self.impulse_y = impulse_y
        self.speed = 0
        self.mass = 0


class Destructable:
    def destroy(self):
        self.entity_container.remove_entity(self)


class Tile(Entity):
    def __init__(self, entity_container: EntityContainer = None):
        Entity.__init__(self, entity_container)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.x_size = 50
        self.y_size = 50


class Wall(Collider, Entity):
    def __init__(self, entity_container: EntityContainer):
        Collider.__init__(self)
        Entity.__init__(self, entity_container)
        self._does_not_collide_with = [Wall]

        if self.entity_container.grid_y % 2 == 0:
            if self.entity_container.grid_x % 2 == 1:
                # Nathan: Horizontaal
                width = 60
                depth = 10
            else:
                # Nathan: Hoekpunt
                width = 40
                depth = 40
        else:
            if self.entity_container.grid_x % 2 == 1:
                # Nathan: Op grid waar tile hoort
                width = 0
                depth = 0
            else:
                # Nathan: Verticaal
                width = 10
                depth = 60
        self.image = pygame.Surface((width, depth))
        self.image.fill((150, 150, 0))
        self.x_size = width
        self.y_size = depth

    def update(self, event_listener, timer_container: TimerContainer):
        pass

class GridMover(Commandable, Entity, Transitional, Updateable):
    def __init__(self, entity_container: EntityContainer):
        Commandable.__init__(self)
        Entity.__init__(self, entity_container)
        Transitional.__init__(self)
        Updateable.__init__(self)


class Player(Collider, GridMover):
    def __init__(self, goal, score, entity_container: EntityContainer = None):
        Collider.__init__(self)
        GridMover.__init__(self, entity_container)
        self.image = pygame.image.load("../images/sized_turtle.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

        # variables to track the transition
        self.transition = WobblyTransition(self)
        self.score = score#TODO LSP violation
        self.goal = goal#TODO LSP violation
        self.goal.player = self

    def update(self, event_listener, timer_container: TimerContainer):
        if self.entity_container.entity_container.in_transition:
            # If we are in transition mode, smoothly transition our world coordinates
            self.transition.transition(event_listener, timer_container)
            # Calculate the distance to the goal
            distance_to_goal = math.sqrt(
                math.pow(
                    (self.entity_container.grid_x - self.goal.entity_container.grid_x), 2
                )
                + math.pow(
                    (self.entity_container.grid_y - self.goal.entity_container.grid_y), 2
                )
            )
            if distance_to_goal <= 0.7:
                # If we are closer than one grid unit to the goal, the goal is eaten and points are scored
                self.goal.eaten = True

    def begin_transition(self):
        # Read a command
        if len(self.command_queue) > 0:
            # If there is a command on the queue, pop it and do it
            command = self.command_queue.pop(0)
            x_change = command[0]
            y_change = command[1]
            if len(self.command_queue) <= 0:
                # If there is no command on the queue tell the grid that it should not play transitions after this one
                self.entity_container.entity_container.play = False
        else:
            x_change = 0
            y_change = 0
            self.entity_container.entity_container.play = False
        # calculate the destination of the transition in grid coordinates
        grid_destination_x = self.entity_container.grid_x + x_change
        grid_destination_y = self.entity_container.grid_y + y_change
        # Define where the transition should stop, shit will also check if the move is possible
        self.transition.define_transition(grid_destination_x, grid_destination_y)


class Enemy(Collider, GridMover):
    def __init__(self, player, entity_container: EntityContainer = None):
        Collider.__init__(self)
        GridMover.__init__(self, entity_container)
        self.image = pygame.image.load("../images/minotaur.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

        # variables to track the transition
        self.transition = CosTransition(self)
        self.player = player#TODO LSP violation

        self.command_queue = [
            [-2, 0],
            [2, 0],
            [2, 0],
            [2, 0],
            [0, 2],
            [2, 0],
            [-2, 0],
            [0, -2],
            [-2, 0],
            [-2, 0],
        ]  # TODO Replace this by a Program instance in the future

        self.command_index = 0  # TODO uitleg: Ik heb dit toegevoegd om bij te houden welk commando er uitevoerd moet worden

        # if len(self.command_queue) > 0:
        #     # If there is a command on the queue, pop it and do it
        #     command = self.command_queue.pop(0)
        #     x_change = command[0]
        #     y_change = command[1]
        # grid_destination_x = self.entity_container.grid_x + x_change
        # grid_destination_y = self.entity_container.grid_y + y_change

    def update(self, event_listener, timer_container: TimerContainer):
        if self.entity_container.entity_container.in_transition:
            # If we are in transition mode, smoothly transition our world coordinates
            self.transition.transition(event_listener, timer_container)

    # def transition(self, event_listener):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    # def define_transition(self, transition_goal_x, transition_goal_y):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    def begin_transition(self):
        # Nathan deze moet nog ingevuld worden hij moet gaan lijken op de begin_transition functie van Player
        # Maar deze functie is helaas nog onleesbaar, ik zal hem meer refactoren zodat het beter te begrijpen is
        # Read a command

        x_change = self.command_queue[self.command_index][0]
        y_change = self.command_queue[self.command_index][1]
        self.command_index += 1
        if self.command_index >= len(self.command_queue):
            self.command_index = 0

        grid_destination_x = self.entity_container.grid_x + x_change
        grid_destination_y = self.entity_container.grid_y + y_change
        # Define where the transition should stop, shit will also check if the move is possible
        self.transition.define_transition(grid_destination_x, grid_destination_y)

        if self.entity_container.grid_x == self.player.entity_container.grid_x:
            # then we have a collision between player and enemy
            pass


class Goal(Collider, GridMover):
    def __init__(self, entity_container: EntityContainer = None):
        Collider.__init__(self)
        GridMover.__init__(self, entity_container)
        self.image = pygame.image.load("../images/lettuce.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.eaten = False#TODO LSP violation
        self.player = None#TODO LSP violation

    def begin_transition(self):
        pass #TODO LSP violation: this has to do something, otherwise it is a violation

    def end_transition(self, timer_container: TimerContainer):
        if self.eaten == True:
            self.player.score.score += 1
            self.player.score.score += 1
            Music.sound_handler("../sounds/munch.wav", 0)
            self.__make_explosion(timer_container)
            self.__respawn()
            self.eaten = False
        self.entity_container.set_grid_xy_to_world_xy(self)

    def __make_explosion(self, timer_container: TimerContainer):#TODO LSP violation resolved?
        for i in range(20):
            angle = uniform(0, 2 * np.pi)
            magnitude = uniform(4, 6)
            particle = Particle(
                self.x,
                self.y,
                np.cos(angle) * magnitude,
                np.sin(angle) * magnitude,
                timer_container,
            )
            self.entity_container.entity_container.add_entity(particle)

    def __respawn(self):#TODO LSP violation resolved?
        while True:
            grid_x = (
                np.random.randint(0, self.entity_container.entity_container.size_x // 2) * 2
                + 1
            )
            grid_y = (
                np.random.randint(0, self.entity_container.entity_container.size_y // 2) * 2
                + 1
            )
            if (
                grid_x != self.entity_container.grid_x
                or grid_y != self.entity_container.grid_y
            ):
                break
        self.entity_container.entity_container.move_grid_entity(self, grid_x, grid_y)


class Score(Entity, Updateable):
    def __init__(self, entity_container: EntityContainer = None):
        GridMover.__init__(self, entity_container)
        self.x = 10
        self.y = 10
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.image = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

    def update(self, event_listener, timer_container: TimerContainer):
        score = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.image = score


class PhysicalEntity(Collider, Entity, Physical, Updateable):
    def __init__(self, x, y, impulse_x, impulse_y, entity_container: EntityContainer = None):
        Collider.__init__(self)
        Entity.__init__(self, entity_container)
        Physical.__init__(self, x, y, impulse_x, impulse_y)
        Updateable.__init__(self)
        self.x = x
        self.y = y


    def update(self, event_listener, timer_container: TimerContainer):
        pass


class Particle(Destructable, PhysicalEntity):
    def __init__(self, x, y, impulse_x, impulse_y, timer_container: TimerContainer, entity_container: EntityContainer = None):
        Destructable.__init__(self)
        PhysicalEntity.__init__(self, x, y, impulse_x, impulse_y, entity_container)
        self.speed = 0
        self.mass = 1
        self.image = pygame.image.load("../images/explosion.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.timer = Timer(1 + uniform(-0.2, 0.2))
        timer_container.append(self.timer)
        self._does_not_collide_with = [Particle, Player]

    def update(self, event_listener, timer_container: TimerContainer):
        self.impulse_x += self.speed * timer_container.time_passed
        if self.timer.check_timer():
            self.destroy()


class Rocket(Destructable, PhysicalEntity):
    def __init__(self, x, y, impulse_x, impulse_y, entity_container: EntityContainer = None):
        Destructable.__init__(self)
        PhysicalEntity.__init__(self, x, y, impulse_x, impulse_y, entity_container)
        self.speed = 40
        self.mass = 1
        self.image = pygame.image.load("../images/pizza-box.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.particle_count = 20
        self.spread = 20
        self.impulse_modifier = 1
        self.impulse_multiplier = 0.1

    def update(self, event_listener, timer_container: TimerContainer):
        #self.update_collisions()#TODO handle this according to commented code
        #if self.collided:
        #    self.make_particles(timer_container)
        #    self.destroy()
        #    self.collided = False
        self.impulse_x += self.speed * timer_container.time_passed

    def destroy(self):
        self.entity_container.remove_entity(self)

    def make_particles(self, timer_container: TimerContainer):
        for i in range(self.particle_count):
            self.entity_container.add_entity(
                Particle(
                    self.x + uniform(-self.spread, self.spread),
                    self.y + uniform(-self.spread, self.spread),
                    self.impulse_x * self.impulse_multiplier
                    + uniform(-self.impulse_modifier, self.impulse_modifier),
                    self.impulse_y * self.impulse_multiplier
                    + uniform(
                        -self.impulse_modifier,
                        self.impulse_modifier,
                        timer_container,
                        self.entity_container,
                    ),
                )
            )


class RocketDuck(PhysicalEntity):
    def __init__(self, x, y, impulse_x, impulse_y, entity_container: EntityContainer = None):
        PhysicalEntity.__init__(self, x, y, impulse_x, impulse_y, entity_container)
        self.speed = 20
        self.mass = 1
        self.image = pygame.image.load("../images/rocket_duck.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.angle = 3 * np.pi / 2
        self.turn_speed = 50

    def update(self, event_listener, timer_container: TimerContainer):
        self.angle += (
            self.turn_speed * np.random.uniform(-1, 1) * timer_container.time_passed
        )
        if self.angle < 0:
            self.angle += 2 * np.pi
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
        self.impulse_x += np.cos(self.angle) * self.speed * timer_container.time_passed
        self.impulse_y += np.sin(self.angle) * self.speed * timer_container.time_passed


class EntityContainer:
    def __init__(self):
        self.entities = []

    def add_entity(self, ent):
        ent.entity_container = self
        self.entities.append(ent)

    def remove_entity(self, ent):
        ent.entity_container = None
        self.entities.remove(ent)

    def update_entities(self, event_listener, timer_container: TimerContainer):
        for ent in self.entities:
            ent.update(event_listener)


class GridPointInfo:
    def __init__(
        self, grid_x, grid_y, zero_x, zero_y, tile_size, wall_size, entity_container: EntityContainer = None
    ):
        self.entity_container = entity_container
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.zero_x = zero_x
        self.zero_y = zero_y
        self.tile_size = tile_size
        self.wall_size = wall_size

    def grid_xy_to_world_xy(self, grid_x, grid_y):
        x = (
            (grid_x // 2) * self.tile_size
            + np.ceil(grid_x / 2) * self.wall_size
            + self.zero_x
        )
        y = (
            (grid_y // 2) * self.tile_size
            + np.ceil(grid_y / 2) * self.wall_size
            + self.zero_y
        )
        return x, y

    def set_grid_xy_to_world_xy(self, ent):
        ent.x, ent.y = self.grid_xy_to_world_xy(self.grid_x, self.grid_y)


class GridPoint(EntityContainer, GridPointInfo):
    def __init__(
        self, grid_x, grid_y, zero_x, zero_y, tile_size, wall_size, entity_container: EntityContainer = None
    ):
        EntityContainer.__init__(self)
        GridPointInfo.__init__(
            self, grid_x, grid_y, zero_x, zero_y, tile_size, wall_size, entity_container
        )


class GridContainer:
    def __init__(self, timer_container: TimerContainer):
        self.size_x = 0
        self.size_y = 0
        self.zero_x = 50
        self.zero_y = 50
        self.tile_size = 50
        self.wall_size = 50
        self.transition_cooldown = 0.3
        self.transition_timer = Timer(0)
        timer_container.append(self.transition_timer)
        self.in_transition = False  # Are we in a transition state?
        self.play = False  # Do we play all commands in the player's queue?
        self.player = None  # can be removed in future
        self.input_cooldown = 0.1  # can be removed in future
        self.input_timer = Timer(0)
        timer_container.append(self.input_timer)  # can be removed in future

        file_name = None
        self.level_builder = LevelBuilder(self)
        self.level_builder.load_level(file_name)
        self.grid = self.level_builder.build_grid()


    def add_grid_entity(self, ent, grid_x, grid_y):
        if isinstance(ent, Player):
            self.player = ent
        self.entities.append(ent)
        self.grid[grid_y][grid_x].add_entity(ent)
        self.grid[grid_y][grid_x].set_grid_xy_to_world_xy(ent)

    def remove_grid_entity(self, ent):
        ent.entity_container.remove_entity(ent)
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

    def move_grid_entity(self, ent, destination_x, destination_y):
        ent.entity_container.remove_entity(ent)
        self.grid[destination_y][destination_x].add_entity(ent)

    def request_move(
        self, grid_source_x, grid_source_y, grid_destination_x, grid_destination_y
    ):
        # TODO Nathan BEGIN
        # Nathan: voordat een entity zich naar een nieuw GridPoint verplaatst, vraagt hij aan grid of dit wel kan / mag
        # Voor nu wordt er alleen gekeken of een entity niet van de grid afloopt
        # Je dit kunnen uitbreiden door te kijken of er een wall tussen de source en destination zit
        # TODO Nathan END
        # print(self.grid[grid_destination_y][grid_destination_x])

        player_within_grid = (
            0 <= grid_destination_x < self.size_x
            and 0 <= grid_destination_y < self.size_y
        )
        player_wall_collision = [
            (grid_destination_x + grid_source_x) / 2,
            (grid_destination_y + grid_source_y) / 2,
        ] in self.all_walls#TODO this should be possible without a self.all_walls variable

        return player_within_grid and not player_wall_collision

    def begin_transition(self, timer_container: TimerContainer):
        if len(self.player.command_queue) <= 0:
            return False
        self.transition_timer = Timer(self.transition_cooldown)
        timer_container.append(self.transition_timer)
        self.in_transition = True
        for ent in self.entities:
            if isinstance(ent, Transitional):
                ent.begin_transition()
        return True

    def end_transition(self, timer_container: TimerContainer):
        self.in_transition = False
        for ent in self.entities:
            if isinstance(ent, Transitional):
                ent.end_transition(timer_container)


class Grid(EntityContainer, GridContainer):
    def __init__(self, timer_container: TimerContainer):
        EntityContainer.__init__(self)
        GridContainer.__init__(self, timer_container)

    def update_entities(self, event_listener, timer_container: TimerContainer):
        # Check the event_listener to see if there is keyboard input
        if (
            self.input_timer.check_timer()
            and not self.play
            and (
                event_listener.K_LEFT
                or event_listener.K_RIGHT
                or event_listener.K_UP
                or event_listener.K_DOWN
            )
        ):
            x_change, y_change = self.check_input(event_listener)
            # If there is input, apply the input by putting a command on the player's queue
            self.player.command_queue.append((x_change, y_change))
            # Set the input_cooldown_timer to better separate individual key presses
            self.input_timer = Timer(self.input_cooldown)
            timer_container.append(self.input_timer)

        # Check if we did not allready start a transition and we are in play mode.
        # If the space bar is pressed when not in a transition, we want to start the play mode.
        # We should not be in the transition mode, because a new transition is initialized
        # A currently running transition should first finish
        if not self.in_transition and (event_listener.K_SPACE or self.play):
            # Set behaviour to play mode. The player can end the play mode once its commands queue is empty
            self.play = self.begin_transition(timer_container)

        # If we are in a transition manage its timer and check if the transition should be stopped
        if self.transition_timer.check_timer() and self.in_transition:
            self.end_transition(timer_container)

        # Ask all entities to update their world coordinates and to do whatever they do
        for ent in self.entities:
            if isinstance(ent, Updateable):
                ent.update(event_listener, timer_container)


class LevelBuilder:
    def __init__(self, grid_container: GridContainer):
        self.grid_container = grid_container


    def load_level(self, file_name: str):
        self.level = np.array(
            [
                "wwwwwwwwwwwwwww",
                "wtntntntntntntw",
                "wnwwwwwnwwwwwnw",
                "wtwtntntwtntwtw",
                "wnwnwwwwwwwnwnw",
                "wtntwtntntntwtw",
                "wnnnwwwwwnnnwnw",
                "wtntntntntntntw",
                "wwwwwwwwwwwwwww",
            ]
        )


    def build_grid(self):
        self.grid_container.size_x = len(self.level[0])
        self.grid_container.size_y = len(self.level)

        # Create the grid
        grid = []
        for i in range(self.grid_container.size_y):
            grid_row = []
            for j in range(self.grid_container.size_x):
                gridPoint = GridPoint(
                    j, i, self.grid_container.zero_x, self.grid_container.zero_y, self.grid_container.tile_size, self.grid_container.wall_size, self.grid_container
                )
                grid_row.append(gridPoint)
            grid.append(grid_row)

        self.grid_container.all_walls = []

        # Fill the grid with Tiles and Walls
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                single_letter = self.level[i][j]
                add_entity = False
                if single_letter == "w":
                    add_entity = True
                    ent = Wall(grid[i][j])
                    self.grid_container.all_walls.append([j,i])
                elif single_letter == "t":
                    add_entity = True
                    ent = Tile(grid[i][j])
                elif single_letter == "n":
                    pass

                if add_entity:
                    self.grid_container.entities.append(ent)
                    grid[i][j].add_entity(ent)
                    grid[i][j].set_grid_xy_to_world_xy(ent)
        return grid