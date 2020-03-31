import math
import numpy as np
from numpy.random import uniform
import pygame
from girlsday_game.music import music
from girlsday_game.transition import CosTransition, InstantTransition, WobblyTransition

class Entity():
    def __init__(self, entity_keeper=None):
        self.entity_keeper = entity_keeper
        self.x = 0
        self.y = 0
        self.image = None
        self.x_size = 0
        self.y_size = 0

    def give_center_xy(self):
        x = self.x - self.x_size / 2
        y = self.y - self.y_size / 2
        return x, y

    def update(self, event_listener):
        pass


class GridEntity(Entity):
    def __init__(self, entity_keeper=None):
        Entity.__init__(self, entity_keeper)
        self.transition = None

    def update(self, event_listener, timer_keeper):
        if self.entity_keeper.entity_keeper.in_transition:
            self.transition.transition(event_listener, timer_keeper)

    def begin_transition(self):
        pass

    def end_transition(self, timer_keeper):
        self.entity_keeper.set_grid_xy_to_world_xy(self)


class Tile(GridEntity):
    def __init__(self, entity_keeper=None):
        GridEntity.__init__(self,entity_keeper)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.x_size = 50
        self.y_size = 50

    def update(self, event_listener, timer_keeper):
        pass

    def begin_transition(self):
        pass


class Wall(GridEntity):
    def __init__(self, entity_keeper):
        GridEntity.__init__(self, entity_keeper)

        # TODO Nathan BEGIN
        # Kijk of je hier meer opties toe kunt voegen en i.p.v. een Surface een Polygon kunt gebruiken
        # Je zou een class van WallShape kunnen maken, maar het lijkt met niet absoluut nodig
        if self.entity_keeper.grid_y % 2 == 0:
            if self.entity_keeper.grid_x % 2 == 1:
                # Nathan: Horizontaal
                width = 60
                depth = 10
            else:
                # Nathan: Hoekpunt
                width = 40
                depth = 40
        else:
            if self.entity_keeper.grid_x % 2 == 1:
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

        # TODO Nathan END

    def update(self, event_listener, timer_keeper):
        pass

    def begin_transition(self):
        pass


class Player(GridEntity):
    def __init__(self, goal, score, entity_keeper=None):
        GridEntity.__init__(self, entity_keeper)
        self.image = pygame.image.load("../images/sized_turtle.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

        # variables to track the transition
        self.transition = WobblyTransition(self)

        self.command_queue = []  # TODO Replace this by a Program instance in the future
        self.score = score
        self.goal = goal
        self.goal.player = self

    def update(self, event_listener, timer_keeper):
        if self.entity_keeper.entity_keeper.in_transition:
            # If we are in transition mode, smoothly transition our world coordinates
            self.transition.transition(event_listener, timer_keeper)
            # Calculate the distance to the goal
            distance_to_goal = math.sqrt(
                math.pow((self.entity_keeper.grid_x - self.goal.entity_keeper.grid_x), 2) + math.pow(
                    (self.entity_keeper.grid_y - self.goal.entity_keeper.grid_y), 2))
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
                self.entity_keeper.entity_keeper.play = False
        else:
            x_change = 0
            y_change = 0
            self.entity_keeper.entity_keeper.play = False
        # calculate the destination of the transition in grid coordinates
        grid_destination_x = self.entity_keeper.grid_x + x_change
        grid_destination_y = self.entity_keeper.grid_y + y_change
        #Define where the transition should stop, shit will also check if the move is possible
        self.transition.define_transition(grid_destination_x, grid_destination_y)


# TODO Nathan BEGIN
# Nathan: Deze functie kan verder uitgebreid worden
class Enemy(GridEntity):
    def __init__(self, Player, entity_keeper=None):
        GridEntity.__init__(self, entity_keeper)
        self.image = pygame.image.load("../images/minotaur.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

        # variables to track the transition
        self.transition = CosTransition(self)
        self.player = Player

        self.command_queue = [[-2,0],[2,0],[2,0],[2,0], [0,2], [2,0], [-2,0], [0,-2], [-2,0], [-2,0]]  # TODO Replace this by a Program instance in the future

        self.command_index = 0 #TODO uitleg: Ik heb dit toegevoegd om bij te houden welk commando er uitevoerd moet worden

        # if len(self.command_queue) > 0:
        #     # If there is a command on the queue, pop it and do it
        #     command = self.command_queue.pop(0)
        #     x_change = command[0]
        #     y_change = command[1]
        # grid_destination_x = self.entity_keeper.grid_x + x_change
        # grid_destination_y = self.entity_keeper.grid_y + y_change

    def update(self, event_listener, timer_keeper):
        if self.entity_keeper.entity_keeper.in_transition:
            # If we are in transition mode, smoothly transition our world coordinates
            self.transition.transition(event_listener, timer_keeper)

    # def transition(self, event_listener):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    # def define_transition(self, transition_goal_x, transition_goal_y):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    def begin_transition(self):
        # Nathan deze moet nog ingevuld worden hij moet gaan lijken op de begin_transition functie van Player
        # Maar deze functie is helaas nog onleesbaar, ik zal hem meer refactoren zodat het beter te begrijpen is
        # Read a command

        #TODO uitleg: gebruik de huidige command_index om het commando op te halen
        x_change = self.command_queue[self.command_index][0]
        y_change = self.command_queue[self.command_index][1]
        #TODO uitleg: voor de volgende transitie, incrementeer de commando_index
        self.command_index += 1
        #TODO uitleg: als de command_index uit de array loopt, wordt hij gereset naar 0 en begint dus van voren af aan
        if self.command_index >= len(self.command_queue):
            self.command_index = 0
        #print(x_change, y_change)

        grid_destination_x = self.entity_keeper.grid_x + x_change
        grid_destination_y = self.entity_keeper.grid_y + y_change
        # Define where the transition should stop, shit will also check if the move is possible
        self.transition.define_transition(grid_destination_x, grid_destination_y)

        if self.entity_keeper.grid_x == self.player.entity_keeper.grid_x:
            # then we have a collision between player and enemy
            pass


# TODO Nathan END

class Goal(GridEntity):
    def __init__(self, entity_keeper=None):
        GridEntity.__init__(self, entity_keeper)
        self.image = pygame.image.load("../images/lettuce.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.eaten = False
        self.player = None

    def update(self, event_listener, timer_keeper):
        pass
        #print(self.eaten)

    def end_transition(self, timer_keeper):
        if self.eaten == True:
            self.player.score.score += 1
            self.player.score.score += 1
            music.sound_handler('../sounds/munch.wav', 0)
            self.make_explosion(timer_keeper)
            self.respawn()
            self.eaten = False
        self.entity_keeper.set_grid_xy_to_world_xy(self)

    def make_explosion(self, timer_keeper):
        for i in range(20):
            angle = uniform(0,2 * np.pi)
            magnitude = uniform(4,6)
            particle = Particle(self.x, self.y, np.cos(angle) * magnitude, np.sin(angle) * magnitude, timer_keeper)
            self.entity_keeper.entity_keeper.add_entity(particle)

    def respawn(self):
        while True:
            grid_x = np.random.randint(0, self.entity_keeper.entity_keeper.size_x // 2) * 2 + 1
            grid_y = np.random.randint(0, self.entity_keeper.entity_keeper.size_y // 2) * 2 + 1
            if grid_x != self.entity_keeper.grid_x or grid_y != self.entity_keeper.grid_y:
                break
        self.entity_keeper.entity_keeper.move_grid_entity(self, grid_x, grid_y)


class Score(GridEntity):
    def __init__(self, entity_keeper=None):
        GridEntity.__init__(self, entity_keeper)
        self.x = 10
        self.y = 10
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.image = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]

    def update(self, event_listener, timer_keeper):
        score = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.image = score


class PhysicalEntity(Entity):
    def __init__(self, x, y, impulse_x, impulse_y, entity_keeper=None):
        Entity.__init__(self, entity_keeper)
        self.x = x
        self.y = y
        self.impulse_x = impulse_x
        self.impulse_y = impulse_y
        self.speed = 0
        self.mass = 0
        self.collided = False

    def update(self, event_listener, timer_keeper):
        pass

    def collision(self):
        pass


class Projectile(PhysicalEntity):
    def __init__(self, x, y, impulse_x, impulse_y, entity_keeper=None):
        PhysicalEntity.__init__(self, x, y, impulse_x, impulse_y, entity_keeper)
        self.speed = 40
        self.mass = 1

    def update(self, event_listener, timer_keeper):
        if self.collided:
            self.collision()
            self.collided = False
        self.impulse_x += self.speed * timer_keeper.time_passed

    def destroy(self):
        self.entity_keeper.remove_entity(self)

    def collision(self):
        self.destroy()


class Particle(Projectile):
    def __init__(self, x, y, impulse_x, impulse_y, timer_keeper, entity_keeper=None):
        Projectile.__init__(self, x, y, impulse_x, impulse_y, entity_keeper)
        self.speed = 0
        self.mass = 1
        self.image = pygame.image.load("../images/explosion.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.timer = timer_keeper.add_timer(1 + uniform(-0.2, 0.2))

    def update(self, event_listener, timer_keeper):
        if self.collided:
            self.collided = False
        self.impulse_x += self.speed * timer_keeper.time_passed
        if self.timer.check_timer():
            self.destroy()


class Rocket(Projectile):
    def __init__(self, x, y, impulse_x, impulse_y, entity_keeper=None):
        Projectile.__init__(self, x, y, impulse_x, impulse_y, entity_keeper)
        self.speed = 40
        self.mass = 1
        self.image = pygame.image.load("../images/pizza-box.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.particle_count = 20
        self.spread = 20
        self.impulse_modifier = 1
        self.impulse_multiplier = 0.1

    def update(self, event_listener, timer_keeper):
        if self.collided:
            self.make_particles(timer_keeper)
            self.destroy()
            self.collided = False
        self.impulse_x += self.speed * timer_keeper.time_passed

    def destroy(self):
        self.entity_keeper.remove_entity(self)

    def collision(self):
        self.destroy()

    def make_particles(self,timer_keeper):
        for i in range(self.particle_count):
            self.entity_keeper.add_entity(Particle(self.x + uniform(-self.spread, self.spread),
                                                 self.y + uniform(-self.spread, self.spread),
                                                 self.impulse_x * self.impulse_multiplier + uniform(
                                                     -self.impulse_modifier, self.impulse_modifier),
                                                 self.impulse_y * self.impulse_multiplier + uniform(
                                                     -self.impulse_modifier, self.impulse_modifier, timer_keeper, self.entity_keeper)))


class RocketDuck(PhysicalEntity):
    def __init__(self, x, y, impulse_x, impulse_y, entity_keeper=None):
        PhysicalEntity.__init__(self, x, y, impulse_x, impulse_y, entity_keeper)
        self.speed = 20
        self.mass = 1
        self.image = pygame.image.load("../images/rocket_duck.png")
        self.x_size = self.image.get_size()[1]
        self.y_size = self.image.get_size()[0]
        self.angle = 3 * np.pi / 2
        self.turn_speed = 50

    def update(self, event_listener, timer_keeper):
        if self.collided:
            self.collision()
            self.collided = False
        self.angle += (
                self.turn_speed * np.random.uniform(-1, 1) * timer_keeper.time_passed
        )
        if self.angle < 0:
            self.angle += 2 * np.pi
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
        self.impulse_x += np.cos(self.angle) * self.speed * timer_keeper.time_passed
        self.impulse_y += np.sin(self.angle) * self.speed * timer_keeper.time_passed

    def collision(self):
        pass
