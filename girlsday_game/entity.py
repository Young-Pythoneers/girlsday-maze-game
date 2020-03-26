import math
import numpy as np
from numpy.random import uniform
import pygame
from girlsday_game.music import music

class Entity:
    def __init__(self, entityKeeper = None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0

    def give_center_XY(self):
        X = self.X - self.X_size / 2
        Y = self.Y - self.Y_size / 2
        return X, Y

    def update(self, event_listener):
        ...


class GridEntity(Entity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_function = lambda x : x

    def update(self, event_listener):
        if self.entityKeeper.entityKeeper.in_transition:
            self.transition(event_listener)

    def transition(self, event_listener):
        time_fraction = self.entityKeeper.entityKeeper.transition_time_counter / self.entityKeeper.entityKeeper.transition_time
        self.X = self.transition_start_X + (self.transition_stop_X - self.transition_start_X) * self.transition_function(time_fraction)
        self.Y = self.transition_start_Y + (self.transition_stop_Y - self.transition_start_Y) * self.transition_function(time_fraction)

    def define_transition(self, transition_goal_X, transition_goal_Y):
        self.transition_start_X = self.X
        self.transition_start_Y = self.Y
        self.transition_stop_X = transition_goal_X
        self.transition_stop_Y = transition_goal_Y

    def begin_transition(self):
        pass

class Tile(GridEntity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.X_size = 50
        self.Y_size = 50
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_function = None

    def update(self, event_listener):
        pass

    def transition(self, event_listener):
        pass

    def define_transition(self, transition_goal_X, transition_goal_Y):
        pass

    def begin_transition(self):
        pass

class Wall(GridEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.width = 0
        self.height = 0

        #TODO Nathan BEGIN
        #Kijk of je hier meer opties toe kunt voegen en i.p.v. een Surface een Polygon kunt gebruiken
        #Je zou een class van WallShape kunnen maken, maar het lijkt met niet absoluut nodig

        # if self.entityKeeper.grid_Y % 2 == 0:
        #     if self.entityKeeper.grid_X % 2 == 1:
        #         #Nathan: Horizontaal
        #         width = 60
        #         depth = 10
        #     else:
        #         #Nathan: Hoekpunt
        #         width = 40
        #         depth = 40
        #
        # else:
        #     if self.entityKeeper.grid_X % 2 == 1:
        #         #Nathan: Op grid waar tile hoort
        #         width = 0
        #         depth = 0
        #     else:
        #         #Nathan: Verticaal
        #         width = 10
        #         depth = 60
        # self.image = pygame.Surface((width, depth))
        # self.image.fill((150, 150, 0))
        # self.X_size = width
        # self.Y_size = depth
        # TODO Nathan END
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_function = None


    def update(self, event_listener):
        pass

    def transition(self, event_listener):
        pass

    def define_transition(self, transition_goal_X, transition_goal_Y):
        pass

    def begin_transition(self):
        pass

class Player(GridEntity):
    def __init__(self, Goal, Score, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.image.load("../images/sized_turtle.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]

        #variables to track the transition
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_function = lambda x : -np.cos(np.pi * x / 2) + 1

        self.command_queue = []#TODO Replace this by a Program instance in the future
        self.score = Score
        self.goal = Goal

    def update(self, event_listener):
        if self.entityKeeper.entityKeeper.in_transition:
            #If we are in transition mode, smoothly transition our world coordinates
            self.transition(event_listener)
        else:
            #If we are not in transition mode, we can check for interactions
            #Calculate the distance to the goal
            distance_to_goal = math.sqrt(
                math.pow((self.entityKeeper.grid_X - self.goal.entityKeeper.grid_X), 2) + math.pow((self.entityKeeper.grid_Y - self.goal.entityKeeper.grid_Y), 2))
            if distance_to_goal <= 0.7:
                #If we are closer than one grid unit to the goal, the goal is eaten and points are scored
                self.goal.eaten = True
                self.score.score += 1
                music.sound_handler('../sounds/munch.wav', 0)
                #TODO Nathan BEGIN
                #Nathan probeer hier eens een aantal particles toe te voegen aan self.entityKeeper.entityKeeper.entities (dit is de Grid)
                #self.entityKeeper is de GridPoint waar Player momenteel is. De entityKeeper van dit GridPoint is dus de Grid
                #Je kunt particles de X en Y van Player meegeven en een random impulse_X en impulse_Y.
                #Dan lijkt het al gauw op een explosie
                #TODO Nathan END

    def begin_transition(self):
        #Read a command
        if len(self.command_queue) > 0:
            # If there is a command on the queue, pop it and do it
            command = self.command_queue.pop(0)
            X_change = command[0]
            Y_change = command[1]
        else:
            # If there is no command on the queue tell the grid that it should not play transitions anymore
            self.entityKeeper.entityKeeper.play = False
            X_change = 0
            Y_change = 0
        #calculate the destination of the transition in grid coordinates
        grid_destination_X = self.entityKeeper.grid_X + X_change
        grid_destination_Y = self.entityKeeper.grid_Y + Y_change
        #Check if the transition to the destination is possible
        if not self.entityKeeper.entityKeeper.requestMove(self.entityKeeper.grid_X, self.entityKeeper.grid_Y, grid_destination_X, grid_destination_Y):
            #If the transition is not possible, a transition is still initialized, but with a change of 0.
            #This way this entity is not moved, but it still waits for one transition interval.
            #This is needed to synchronize all transitioning entities.
            grid_destination_X = self.entityKeeper.grid_X
            grid_destination_Y = self.entityKeeper.grid_Y
        #Register the new grid position for the move
        self.entityKeeper.entityKeeper.moveGridEntity(self, grid_destination_X, grid_destination_Y)
        #Calculate the destination in world coordinates
        destination_X, destination_Y = self.entityKeeper.grid_XY_to_world_XY(grid_destination_X, grid_destination_Y)
        #Remember the destination world coordinates in order to perform a smooth transition
        self.define_transition(destination_X, destination_Y)

#TODO Nathan BEGIN
#Nathan: Deze functie kan verder uitgebreidt worden
class Enemy(GridEntity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_function = lambda x : x

    def update(self, event_listener):
        if self.entityKeeper.entityKeeper.in_transition:
            self.transition(event_listener)

    #def transition(self, event_listener):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    #def define_transition(self, transition_goal_X, transition_goal_Y):#Nathan deze functie wordt geerfd van GridEntity, dus hoeft niet opnieuw gedefinieerd te worden

    def begin_transition(self):
        #Nathan deze moet nog ingevuld worden hij moet gaan lijken op de begin_transition functie van Player
        #Maar deze functie is helaas nog onleesbaar, ik zal hem meer refactoren zodat het beter te begrijpen is
        pass
#TODO Nathan END

class Goal(GridEntity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.entityKeeper = None
        self.X = 0
        self.Y = 0
        self.image = pygame.image.load("../images/lettuce.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.eaten = False


    def update(self, event_listener):
        if self.eaten == True:
            self.respawn()
            self.eaten = False

    def respawn(self):
        while True:
            grid_X = np.random.randint(0, 7) * 2 + 1
            grid_Y = np.random.randint(0, 5) * 2 + 1
            if grid_X != self.entityKeeper.grid_X and grid_Y != self.entityKeeper.grid_Y:
                break
        self.entityKeeper.entityKeeper.moveGridEntity(self, grid_X, grid_Y)

class Score(GridEntity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.entityKeeper = None
        self.X = 10
        self.Y = 10
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.image = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]

    def update(self, event_listener):
        score = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.image = score


class PhysicalEntity(Entity):
    def __init__(self, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.entityKeeper = None
        self.X = 0
        self.Y = 0
        self.impulse_X = 0
        self.impulse_Y = 0
        self.speed = 0
        self.mass = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.collided = False

    def update(self, event_listener):
        ...

    def collision(self):
        ...

class Projectile(PhysicalEntity):
    def __init__(self, X, Y, impulse_X, impulse_Y, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 40
        self.mass = 1
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.collided = False

    def update(self, event_listener):
        if self.collided:
            self.collision()
            self.collided = False
        self.impulse_X += self.speed * event_listener.time_passed

    def destroy(self):
        self.entityKeeper.removeEntity(self)

    def collision(self):
        self.destroy()

class Particle(Projectile):
    def __init__(self, X, Y, impulse_X, impulse_Y, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 0
        self.mass = 0.1
        self.image = pygame.image.load("../images/explosion.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.collided = False
        self.life_time = 0.25 + uniform(-0.1,0.1)

    def update(self, event_listener):
        if self.collided:
            if self.collided:
                self.destroy()
        self.impulse_X += self.speed * event_listener.time_passed
        self.life_time -= event_listener.time_passed
        if not self.collided and  self.life_time < 0:
            self.destroy()

class Rocket(Projectile):
    def __init__(self, X, Y, impulse_X, impulse_Y, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 40
        self.mass = 1
        self.image = pygame.image.load("../images/pizza-box.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.collided = False
        self.particle_count = 20
        self.spread = 20
        self.impulse_modifier = 1
        self.impulse_multiplier = 0.1

    def update(self, event_listener):
        if self.collided:
            self.make_particles()
            self.destroy()
            self.collided = False
        self.impulse_X += self.speed * event_listener.time_passed


    def destroy(self):
        self.entityKeeper.removeEntity(self)

    def collision(self):
        self.destroy()

    def make_particles(self):
        for i in range(self.particle_count):
            self.entityKeeper.addEntity(Particle(self.entityKeeper, self.X + uniform(-self.spread,self.spread), self.Y + uniform(-self.spread,self.spread), self.impulse_X * self.impulse_multiplier + uniform(-self.impulse_modifier, self.impulse_modifier), self.impulse_Y * self.impulse_multiplier + uniform(-self.impulse_modifier, self.impulse_modifier)))

class RocketDuck(PhysicalEntity):
    def __init__(self, X, Y, impulse_X, impulse_Y, entityKeeper=None):
        if entityKeeper is None:
            self.entityKeeper = None
        else:
            self.entityKeeper = entityKeeper
        self.X = 370
        self.Y = 480
        self.impulse_X = 0
        self.impulse_Y = 0
        self.speed = 20
        self.mass = 1
        self.image = pygame.image.load("../images/rocket_duck.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.angle = 3 * np.pi / 2
        self.turn_speed = 50
        self.collided = False

    def update(self, event_listener):
        if self.collided:
            self.collision()
            self.collided = False
        self.angle += (
            self.turn_speed * np.random.uniform(-1, 1) * event_listener.time_passed
        )
        if self.angle < 0:
            self.angle += 2 * np.pi
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
        self.impulse_X += np.cos(self.angle) * self.speed * event_listener.time_passed
        self.impulse_Y += np.sin(self.angle) * self.speed * event_listener.time_passed


    def collision(self):
        pass